# Tianyan Question-Type Routing Index

Use this index before opening any detailed module. Preserve the user's exact
question, select one primary category, and add at most two secondary categories
only when the question genuinely asks a second dimension.

| Category ID | Chinese Label | Module | Inclusion Cues | Exclusion Cues | Common Secondary Categories |
|---|---|---|---|---|---|
| `people-identity` | 人物身份/同伴 | [people-identity.md](people-identity.md) | 谁、和谁、哪个人、同伴、身份、对象 | 问对方想法转 thoughts-intentions；问恋爱关系转 romance-marriage | `romance-marriage`, `travel-whereabouts`, `family-relatives` |
| `thoughts-intentions` | 想法/态度/意图 | [thoughts-intentions.md](thoughts-intentions.md) | 怎么想、态度、意向、打算、心里 | 真实行动转 contact-actions；关系结果转 romance-marriage | `contact-actions`, `romance-marriage`, `travel-whereabouts` |
| `romance-marriage` | 感情/婚恋 | [romance-marriage.md](romance-marriage.md) | 喜欢、复合、分手、恋爱、婚姻、暧昧 | 单纯联系转 contact-actions；单纯身份转 people-identity | `contact-actions`, `thoughts-intentions` |
| `contact-actions` | 联系/行动 | [contact-actions.md](contact-actions.md) | 会不会联系、回复、来找、行动、执行 | 想法不等于行动；结果成败转 outcomes-development | `thoughts-intentions`, `timing`, `strategy-comparison` |
| `location-direction` | 方位/地点 | [location-direction.md](location-direction.md) | 在哪里、方位、方向、位置、地点 | 旅行过程转 travel-whereabouts；遗失物转 objects-lost-property | `travel-whereabouts`, `objects-lost-property` |
| `timing` | 时间/应期 | [timing.md](timing.md) | 什么时候、多久、哪天、何时、有消息 | 只问成败转 outcomes-development；只问行动转 contact-actions | `contact-actions`, `travel-whereabouts`, `contracts-documents` |
| `objects-lost-property` | 物品/遗失物 | [objects-lost-property.md](objects-lost-property.md) | 拿着什么、东西在哪、丢失物、物品类别 | 地点主问转 location-direction；钱款转 money-debt | `location-direction`, `timing` |
| `travel-whereabouts` | 出行/行踪 | [travel-whereabouts.md](travel-whereabouts.md) | 去哪玩、出发、返回、路线、人在外 | 方位主问转 location-direction；时间主问转 timing | `location-direction`, `timing`, `people-identity` |
| `work-career` | 工作/职业 | [work-career.md](work-career.md) | 工作、面试、领导、岗位、升职、职场 | 钱款主问转 money-debt；合同手续转 contracts-documents | `thoughts-intentions`, `contracts-documents` |
| `money-debt` | 钱财/债务 | [money-debt.md](money-debt.md) | 收款、欠款、破财、收益、资金、债 | 合作关系转 business-partnership；合同文件转 contracts-documents | `timing`, `business-partnership` |
| `business-partnership` | 合作/合伙 | [business-partnership.md](business-partnership.md) | 项目、合作、合伙、伙伴、客户、供应商 | 单纯合同转 contracts-documents；单纯钱款转 money-debt | `money-debt`, `contracts-documents` |
| `contracts-documents` | 合同/证件/手续 | [contracts-documents.md](contracts-documents.md) | 合同、协议、证件、审批、手续、材料 | 房产主问转 housing-property；考试录取转 study-exams | `timing`, `housing-property`, `business-partnership` |
| `study-exams` | 学业/考试 | [study-exams.md](study-exams.md) | 考试、录取、学习、复习、证书、成绩 | 工作面试转 work-career；证件审批转 contracts-documents | `timing`, `strategy-comparison` |
| `health-medicine` | 健康/医疗 | [health-medicine.md](health-medicine.md) | 身体、症状、检查、治疗、药、病 | 家庭关系转 family-relatives；孩子健康可加 children-pregnancy | `family-relatives`, `children-pregnancy` |
| `family-relatives` | 家庭/亲属 | [family-relatives.md](family-relatives.md) | 父母、亲戚、家里、家庭矛盾、长辈 | 恋爱转 romance-marriage；钱款主问转 money-debt | `money-debt`, `health-medicine` |
| `children-pregnancy` | 子女/孕育 | [children-pregnancy.md](children-pregnancy.md) | 孩子、子女、备孕、怀孕、入园、胎孕 | 医疗主问转 health-medicine；学业主问转 study-exams | `health-medicine`, `study-exams` |
| `housing-property` | 房屋/房产 | [housing-property.md](housing-property.md) | 买房、卖房、租房、房产证、房屋缺陷 | 合同手续主问转 contracts-documents；钱款转 money-debt | `contracts-documents`, `money-debt`, `timing` |
| `disputes-litigation` | 纠纷/诉讼 | [disputes-litigation.md](disputes-litigation.md) | 纠纷、投诉、官司、证据、调解、仲裁 | 单纯合同转 contracts-documents；工作冲突转 work-career | `contracts-documents`, `strategy-comparison` |
| `outcomes-development` | 成败/发展 | [outcomes-development.md](outcomes-development.md) | 能不能成、有没有转机、结果、发展、走势 | 不得作为无法分类的兜底；具体事项优先转专门模块 | `timing`, `strategy-comparison` |
| `strategy-comparison` | 策略/选择 | [strategy-comparison.md](strategy-comparison.md) | 怎么办、选A还是B、主动还是等、继续还是停 | 单纯预测转对应事项模块；不要为每个选项重复起卦 | `outcomes-development`, `contracts-documents`, `contact-actions` |
