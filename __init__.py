from modules import cbpi
import requests

bf_uri = "http://log.brewfather.net/stream"

def bf_api_id():
  api_id = cbpi.get_config_parameter("brewfather_api_id", None)
  if api_id is None:
    try:
      cbpi.add_config_parameter("brewfather_api_id", "", "text", "Brewfather API Id")
      return ""
    except:
      cbpi.notify("Brewfather Error", "Unable to update brewfather_api_id parameter within database. Try updating CraftBeerPi and reboot.", type="danger", timeout=None)
  else:
    return api_id


@cbpi.backgroundtask(key="brewfather_task", interval=900)
def brewfather_background_task(api):
  api_id = bf_api_id()
  if api_id == "":
    cbpi.notify("Brewfather Error", "Id not set. Update brewfather_api_id parameter within System > Parameters.", type="danger", timeout=None)
    return

  for i, fermenter in cbpi.cache.get("fermenter").iteritems():
    if fermenter.state is not False:
      try:
        name = fermenter.name
        temp = fermenter.instance.get_temp()
        #auxtemp = cbpi.get_sensor_value(int(fermenter.sensor2))
        #exttemp = cbpi.get_sensor_value(int(fermenter.sensor3))
        #brewname = fermenter.brewname
        unit = cbpi.get_config_parameter("unit", "C")
        
        data = {
          "name": name, 
          "temp": temp, 
          #"aux_temp": auxtemp,
          #"ext_temp": exttemp, 
          "temp_unit": unit
          #"beer": brewname
        }

        querystring = {"id": api_id }

        response = requests.post(bf_uri, json=data, params=querystring)

        if response.status_code != 200:
          cbpi.notify("Brewfather Error", "Received unsuccessful response. Ensure API Id is correct. HTTP Error Code: " + str(response.status_code), type="danger", timeout=None)
      except:
        cbpi.notify("Brewfather Error", "Unable to send message.", type="danger", timeout=None)
        pass
