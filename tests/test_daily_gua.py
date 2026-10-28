import concurrent.futures,json,tempfile,unittest
from datetime import datetime,timedelta
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
from daily_gua.storage import GuaStore
from daily_gua.service import DailyGuaService
from daily_gua.presentation import chart_text,audit_text
from scripts.qi_gua import build_cast
from scripts.pai_gua import build_chart

class DailyQuotaTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'gua.sqlite3'
        self.now=datetime(2026,10,28,12,30,tzinfo=ZoneInfo('Asia/Shanghai'))
        self.service=DailyGuaService(GuaStore(self.path),now=lambda:self.now)
    def tearDown(self):self.tmp.cleanup()
    def test_once_persists_after_restart_and_changed_question_city_timezone(self):
        first,one=self.service.draw('user:A','学习安排','北京')
        self.assertTrue(first);self.assertEqual(one['status'],'ready')
        restarted=DailyGuaService(GuaStore(self.path),now=lambda:self.now)
        again,two=restarted.draw('user:A','想换个问题','上海','Pacific/Honolulu')
        self.assertFalse(again);self.assertEqual(one,two)
        self.assertEqual(one['chart']['location'],'北京');self.assertEqual(one['cast']['location'],'北京')
    def test_each_person_and_whale_have_independent_slots(self):
        self.assertTrue(self.service.draw('user:A',location='上海')[0])
        self.assertTrue(self.service.draw('user:B',location='成都')[0])
        fresh,own=self.service.draw('fish:self')
        self.assertTrue(fresh);self.assertEqual(own['location'],'北京')
        self.assertFalse(self.service.draw('fish:self')[0])
    def test_no_city_or_invalid_timezone_consumes_no_quota(self):
        for kwargs in [{},{'location':'北京','timezone':'Invalid/Zone'}]:
            with self.assertRaises((ValueError,KeyError)):self.service.draw('user:A',**kwargs)
            self.assertIsNone(self.service.today('user:A'))
    def test_city_is_saved_and_missing_question_uses_daily_scope(self):
        self.service.set_location('user:A','北京')
        fresh,one=self.service.draw('user:A')
        self.assertTrue(fresh);self.assertEqual(one['location'],'北京')
        self.now+=timedelta(days=1)
        self.assertTrue(self.service.draw('user:A')[0])
    def test_2300_calendar_change_does_not_reset_quota(self):
        self.now=self.now.replace(hour=22,minute=59)
        _,one=self.service.draw('user:A',location='北京')
        self.now=self.now.replace(hour=23,minute=1)
        self.assertFalse(self.service.draw('user:A',location='北京')[0])
        _,other=self.service.draw('user:B',location='北京')
        self.assertNotEqual(one['chart']['calendar']['day'],other['chart']['calendar']['day'])
        self.now=(self.now+timedelta(days=1)).replace(hour=0,minute=1)
        self.assertTrue(self.service.draw('user:A',location='北京')[0])
    def test_concurrent_requests_generate_entropy_once(self):
        original=build_cast
        with patch('daily_gua.service.build_cast',wraps=original) as casting:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                rows=list(pool.map(lambda _:self.service.draw('user:A',location='北京'),range(8)))
        self.assertEqual(sum(fresh for fresh,_ in rows),1)
        self.assertEqual(casting.call_count,1)
        final=self.service.today('user:A');self.assertEqual(final['status'],'ready')
    def test_original_entropy_replays_all_eighteen_coins(self):
        _,one=self.service.draw('user:A',location='北京');cast=one['cast']
        replay=build_cast(cast['question'],cast['timezone'],entropy=bytes.fromhex(cast['entropy_hex']),moment=datetime.fromisoformat(cast['cast_time']).replace(tzinfo=ZoneInfo(cast['timezone'])),mode='replay',location=one['location'])
        self.assertEqual(replay['throws'],cast['throws'])
        self.assertEqual(len(cast['throws']),6)
        self.assertTrue(all(len(t['coins'])==3 for t in cast['throws']))
    def test_failure_after_entropy_preserves_original_cast_and_recovers_without_reroll(self):
        with patch('daily_gua.service.build_chart',side_effect=RuntimeError('offline test')):
            _,one=self.service.draw('user:A',location='北京')
        self.assertEqual(one['status'],'failed');self.assertIn('cast',one)
        with patch('daily_gua.service.build_cast',side_effect=AssertionError('never reroll')):
            recovered=self.service.recover_chart('user:A')
        self.assertEqual(recovered['status'],'ready')
        self.assertEqual(recovered['cast'],one['cast'])
    def test_abandoned_reservation_does_not_trigger_second_cast(self):
        self.service.store.reserve('user:A',self.now.date(),{'status':'reserved'})
        with patch('daily_gua.service.build_cast',side_effect=AssertionError('never reroll')):
            fresh,one=self.service.draw('user:A',location='北京')
        self.assertFalse(fresh);self.assertEqual(one['status'],'reserved')
    def test_manual_values_preserved_and_count_towards_same_limit(self):
        _,one=self.service.draw('user:A','学习安排','北京',lines='6 7 8 9 7 8',cast_time='2026-10-27 18:30')
        self.assertEqual(one['chart']['line_values'],[6,7,8,9,7,8])
        self.assertEqual(one['cast']['method'],'user_supplied')
        self.assertNotIn('entropy_hex',one['cast'])
        self.assertEqual(one['date'],'2026-10-28')
        self.assertFalse(self.service.draw('user:A',location='北京')[0])
    def test_automatic_cast_ignores_no_fake_historical_dates(self):
        with self.assertRaises(ValueError):self.service.draw('user:A',location='北京',cast_time='2020-01-01 12:00')
        self.assertIsNone(self.service.today('user:A'))
    def test_chart_details_and_audit_are_not_language_model_fabrications(self):
        _,record=self.service.draw('user:A',location='北京')
        chart=record['chart']
        again=build_chart(record['question'],record['cast']['cast_time'],record['timezone'],record['cast']['line_values'],location='北京')
        self.assertEqual(chart,again)
        text=chart_text(record);audit=audit_text(record)
        for word in ['世','旬空','月建','日辰','北京','2026-10-28']:self.assertIn(word,text)
        self.assertIn(record['cast']['entropy_hex'],audit)
        self.assertEqual(len(chart['lines']),6)
    def test_user_cannot_modify_whale_location(self):
        with self.assertRaises(ValueError):self.service.draw('fish:self',location='上海')
        with self.assertRaises(ValueError):self.service.set_location('fish:self','上海')
        self.assertIsNone(self.service.today('fish:self'))
