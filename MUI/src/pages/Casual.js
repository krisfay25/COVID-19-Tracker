import { useEffect, useCallback, useState } from 'react';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet'
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';

function Casual(props) {
  // boolean for when polygonCoor has been populated and is ready to render
  const [ready, setReady] = useState(false);
  // this is where all of the values for the polygons will be kept
  const [polygonCoor, setPolygonCoor] = useState([]);

  // originally, the coordinates are in the wrong format. 
  // makes coordinates [x,y] => [y,x]
  const swapCoor = useCallback((data) => {
    for (let group of data) {
      if (group.geometry.type === "Polygon") {
        // Swap Polygon coordinates
        for (let polygon of group.geometry.coordinates) {
          for (let coord of polygon) {
            let temp = coord[0];
            coord[0] = coord[1];
            coord[1] = temp;
          }
        }
      } else if (group.geometry.type === "MultiPolygon") {
        // Swap the coordinates for each Polygon in a MultiPolygon
        for (let multiPolygon of group.geometry.coordinates) {
          for (let polygon of multiPolygon) {
            for (let coord of polygon) {
              let temp = coord[0];
              coord[0] = coord[1];
              coord[1] = temp;
            }
          }
        }
      }
    }
  }, []);

  // sets the polygonCoor with the data fetched from the backend. also sets id and color
  // new parameters can be added here
  const setCoor = useCallback((data) => {
    setPolygonCoor([{"id": "001", "color": "red", "coordinates": data[0].geometry.coordinates},
      {"id": "003", "color": "blue", "coordinates": data[1].geometry.coordinates},
      {"id": "005", "color": "green", "coordinates": data[2].geometry.coordinates},
      {"id": "007", "color": "yellow", "coordinates": data[3].geometry.coordinates},
      {"id": "009", "color": "purple", "coordinates": data[4].geometry.coordinates},
    ]);
  }, []);

  useEffect(() => {
    async function getData () {
      const response = await axios.get("http://localhost:5000/all/geo_json_data");
      swapCoor(response.data);
      setCoor(response.data);
      setReady(true);
    };
    getData();
  }, [setCoor, swapCoor]);
  
  return (
    <div>
    {ready
      ? <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
        <TemporaryDrawer/>
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {polygonCoor
          ? polygonCoor.map((coor) => (
            <Polygon positions={coor.coordinates} color={coor.color} key={coor.id}>
              <Popup>
                {coor.id}
              </Popup>
            </Polygon>
          ))
          : <></>
        }
        </MapContainer>
      : <p>Loading....</p>
    }
     
    </div>

  );
};

export default Casual;
