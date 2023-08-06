=============================================
Valicoc - Validation Code Check and save
=============================================
This module uses module `re` to match more-than-four-digits-validation-code
+-------------------+------------+
|      Message      |   Result   |
+===================+============+
| ��***�����ã����� |            |
| ��¼��֤��Ϊ103562|   103562   |
| ����ע�����      |            |
+-------------------+------------+
| ��***��������֤�� |            |
| 806549������ʮ��  |   806549   |
| ���������֤��    |            |
+-------------------+------------+
...

Usage:
`import valicoc
valicoc.get("Your message")`

This module is only for Chinese messages, and messages have to have
keyword `��֤��`.
