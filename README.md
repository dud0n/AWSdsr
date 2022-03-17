# AWSdsr

AWSdsr - утилитка для AWS, листинг объектов в аккаунте по всем доступным регионам. Для работы необходим python >= 3.7 и awscli2 (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html)

На сегодня для поиска доступны: Instance, VPC, Elastic IP

## Use
awsdsr -h

awsdsr --profile [profilename] --freetire -o [objects ...]

objects: instance vpc eip

Наличие в строке запуска ключа --freetire включит предупреждения возможного перерасхода бесплатного  тестового периода аккаунта (пока актуально для instance > 2, потенциально израсходует время работы instance за 14 дней вместо 1 месяца). По мере роста утилиты буду дописывать объекты, для которых актуальны предупреждения.

Нет ключа - нет предупреждений!

Для Elastic IP предупреждения выводятся всегда, если зарезервированный IP не имеет привязки к instance или iface.

