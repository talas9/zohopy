"""Example script — demonstrates using ZohoPy in Docker or standalone."""

from zohopy import SyncZohoClient, ZohoConfig
from zohopy.logging import configure_logging, get_logger
from zohopy.products.books import ZohoBooks

configure_logging()
logger = get_logger()


def main() -> None:
    config = ZohoConfig()
    logger.info("connecting", data_center=config.data_center.value)

    with SyncZohoClient(config) as client:
        books = ZohoBooks(client)

        result = books.organizations.list()
        orgs = result.get("organizations", [])
        logger.info("organizations.listed", count=len(orgs))

        for org in orgs:
            logger.info(
                "organization",
                name=org.get("name"),
                org_id=org.get("organization_id"),
            )


if __name__ == "__main__":
    main()
