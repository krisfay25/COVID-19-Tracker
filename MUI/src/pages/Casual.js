import React from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import PropTypes from 'prop-types'
import './leaflet/Casual.css';
import './leaflet/counties_geoJSON.js';

function Casual(props) {
  return (
    <>
      <MapContainer center={[41.700, -71.500]} zoom={9} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[41.700, -71.500]}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>

      </MapContainer>
      </>
  );
}


export default Casual;

