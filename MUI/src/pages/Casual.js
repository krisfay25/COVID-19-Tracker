import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'
import './leaflet/Casual.css';
import './leaflet/counties_geoJSON.js';
import TemporaryDrawer from '../components/TemporaryDrawer';


//Getting Data
const  getData = () => {
  fetch('http://localhost:5000/all/geo_json_data', {
      headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
      }
  }).then(response=>response.json())
  .then(data => {
      console.log(data)
      setMain(data);
  });
}
useEffect(() => {
  getData()
},[])

function Casual(props) {
    return (
        <div>
          <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
          <TemporaryDrawer/>
          <TileLayer
           attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <Polygon positions={coords}/>
          </MapContainer>
        </div>
      
  );
}


export default Casual;

