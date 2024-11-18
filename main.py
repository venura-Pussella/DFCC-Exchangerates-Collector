import asyncio
import platform
from src import logger
from src.utils.log_utils import send_log
from src.configuration.configuration import Basefile_name
from src.connector.fetch_url import fetch_url
from src.operators.html_to_dataframe import process_html_content
from src.operators.dataframe_to_csvdata import write_exchange_rates_to_csv_data
from src.connector.blob import upload_to_blob
from src.operators.convert_to_cosmosdb import convert_df_to_cosmos_db_format
from src.connector.cosmosdb_ import write_exchange_rates_to_cosmosdb
# from src.operators.playwright_helper import install_playwright_browser_binaries

async def main():
    try :
        logger.info("Starting DFCC Bank Exchangerates Collector")

        # # Function to install playwright browser binaries
        # install_playwright_browser_binaries()

        # Extract html content from Url
        data = await fetch_url()
        logger.info("Extracted html content.")

        # Process data
        exchange_rates_df = process_html_content(data)
        logger.info("Dataframe created.")

        # Convert DataFrame to CSV data string
        csv_data = write_exchange_rates_to_csv_data(exchange_rates_df)
        logger.info("CSV data created.")

        # Upload CSV data to Blob Storage
        upload_to_blob(csv_data, Basefile_name)
        logger.info("Successfully uploaded to blob.")

        # Convert to JSON format
        cosmos_db_documents_json = convert_df_to_cosmos_db_format(exchange_rates_df)
        logger.info("Successfully converted DataFrame to Cosmos DB format.")

        # Upload to Cosmos DB
        await write_exchange_rates_to_cosmosdb(cosmos_db_documents_json)
        logger.info("Completion of data ingestion to Cosmos DB.")

    #     # Send_log to monitoring service
    #     send_log(

    #         service_type="Azure Function",
    #         application_name="DFCC Exchangerates Collector",
    #         project_name="Dockit Exchange Rates History",
    #         project_sub_name="Exchangerates History",
    #         azure_hosting_name="AI Services",
    #         developmental_language="Python",
    #         description="Bank Exchange Rates - Function Application",
    #         created_by="BrownsAIseviceTest",
    #         log_print="Successfully completed data ingestion to Cosmos DB.",
    #         running_within_minutes=1440,
    #         error_id=0

    #     )
    #     logger.info("sent success log to function monitoring service.")

    except Exception as e:
        # send_error_log to monitoring service
        logger.error(f"An error occurred: {e}")

    #     send_log(
    #         service_type="Azure Function",
    #         application_name="DFCC Exchangerates Collector",
    #         project_name="Dockit Exchange Rates History",
    #         project_sub_name="Exchangerates History",
    #         azure_hosting_name="AI Services",
    #         developmental_language="Python",
    #         description="Bank Exchange Rates - Function Application",
    #         created_by="BrownsAIseviceTest",
    #         log_print="An error occurred: " + str(e),
    #         running_within_minutes=1440,
    #         error_id=1,
    #         # SMSSenderGroupId=2
    #     )

        raise
def run_main():

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    # asyncio.run(main())

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == '__main__':
    run_main()
