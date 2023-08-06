=============================================
Valicoc - Validation Code Check and save
=============================================
This module uses module `re` to match more-than-four-digits-validation-code
+-------------------+------------+
|      Message      |   Result   |
+===================+============+
| 【***】您好，本次 |            |
| 登录验证码为103562|   103562   |
| ，请注意查收      |            |
+-------------------+------------+
| 【***】短信验证码 |            |
| 806549，请在十分  |   806549   |
| 钟内完成验证。    |            |
+-------------------+------------+
...

Usage:
`import valicoc
valicoc.get("Your message")`

This module is only for Chinese messages, and messages have to have
keyword `验证码`.
