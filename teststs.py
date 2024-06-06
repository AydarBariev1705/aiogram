import pandas as pd
import os
final_dict = {
        'name': 'Test1',
        'phone_number': 'Test',
        'total_amount': 'Test',
        'currency': 'Test',
        'telegram_payment_charge_id': 'Test',
        'provider_payment_charge_id': 'Test',
        'shipping_address': 'Test',
        'date': 'Test'
    }
df_new = pd.DataFrame(final_dict, index=[0])
# df_old = pd.read_excel('twtee1.xlsx')
if not os.path.exists(f'twtee1.xlsx'):
    df_old = pd.DataFrame({})
else:
    df_old = pd.read_excel('twtee1.xlsx')
df3 = pd.concat([df_new, df_old])
df3.to_excel(excel_writer=f'twtee1.xlsx', sheet_name='awdawd', index=False)

#view resulting DataFrame
print(df3)
# print(type(df_old))
# print(type(df_new))
# # df_final = pd.concat([
# #     df_old,
# #     df_new
# # ])
#
# df_final.to_excel(excel_writer=f'twtee.xlsx', sheet_name='awdawd', index=False)
