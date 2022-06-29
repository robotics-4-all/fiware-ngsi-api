from fiware_ngsi_api.configuration import NgsiConfiguration
from fiware_ngsi_api.api_client import NgsiApiClient

from fiware_ngsi_api.models.slot_api import NgsiSlotAPI

if __name__ == "__main__":
    config = NgsiConfiguration("../../conf/settings.conf")
    client = NgsiApiClient(configuration=config)

    with NgsiSlotAPI(client, "../../data-models/slot.yaml") as slot:
        slot.width = 10
        slot.originx = 0.8

        response = slot.list_all()

        print(response)
