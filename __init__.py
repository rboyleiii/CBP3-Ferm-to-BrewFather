from modules import cbpi
import requests

bf_uri = "http://log.brewfather.net/stream"

def bf_stream_id ():
  api_id = cbpi.get_config_parameter("brewfather_stream_id", None)
  if api_id is None:
    try:
      cbpi.add_config_parameter("brewfather_stream_id", "", "text", "Brewfather stream API ID")
      return ""
    except:
      cbpi.notify("Brewfather Error", "Unable to update brewfather_stream_id parameter within database. Try updating CraftBeerPi and reboot.", type="danger", timeout=None)
  else:
    return api_id


@cbpi.backgroundtask(key="brewfather_task", interval=900)
def brewfather_background_task(api):
  api_id = bf_stream_id()
  if api_id == "":
    cbpi.notify("Brewfather Error", "Stream ID not set. Update brewfather_stream_id parameter within System > Parameters.", type="danger", timeout=None)
    return

  for i, fermenter in cbpi.cache.get("fermenter").iteritems():

    # if fermenter is active, we will log the temperatures
    if fermenter.state is not False:
      try:
        queryString = {
          "id": api_id
        }
        
        data = {
          "name": fermenter.name,
          "beer": fermenter.brewname,
          "temp": cbpi.get_sensor_value(fermenter.sensor), 
          "aux_temp": cbpi.get_sensor_value(fermenter.sensor2), 
          "ext_temp": cbpi.get_sensor_value(fermenter.sensor3), 
          "temp_unit": cbpi.get_config_parameter("unit", "C")
        }

        response = requests.post(bf_uri, params=queryString, json=data)

        if response.status_code != 200:
          cbpi.notify("Brewfather Error", "Received unsuccessful response. Ensure API Id is correct. HTTP Error Code: " + str(response.status_code), type="danger", timeout=None)

      except BaseException as error:
        cbpi.notify("Brewfather Error", "Unable to send message." + str(error), type="danger", timeout=None)
        pass
