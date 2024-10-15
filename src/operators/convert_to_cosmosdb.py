import uuid

def convert_df_to_cosmos_db_format(df):
    cosmos_db_documents = []
    for _, row in df.iterrows():
        rate_document = {
            "id": str(uuid.uuid4()),
            "timestamp": f"{row['Date']}T{row['Time']}Z",
            "code": row['Currency Type'],
            "dd_buying": float(row['DD Buying']) if row['DD Buying'] else None,
            "currency_note_encashment": float(row['Currency Note Encashment']) if row['Currency Note Encashment'] else None,
            "tt_buying": float(row['TT Buying']) if row['TT Buying'] else None,
            "dd_tt_selling": float(row['DD / TT Selling']) if row['DD / TT Selling'] else None,
            "currency_note_selling": float(row['Currency Note Selling']) if row['Currency Note Selling'] else None,
            "bank": row['Bank'],
            "st_bank_code": row['ST BANK CODE']
        }
        cosmos_db_documents.append(rate_document)
    
    return cosmos_db_documents
