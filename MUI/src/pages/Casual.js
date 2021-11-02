import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'
import './leaflet/Casual.css';
import './leaflet/counties_geoJSON.js';
import TemporaryDrawer from '../components/TemporaryDrawer';


      

function Casual(props) {
    return (
        <div>
          <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
          <TemporaryDrawer/>
          <TileLayer
           attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          </MapContainer>
        </div>
      
  );
}


export default Casual;

