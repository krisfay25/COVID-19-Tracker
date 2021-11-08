import React, { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Polygon, GeoJSON } from 'react-leaflet'
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';

//API call to retrive geoJSON data
const RetrieveData = () => {
  const [data, setData] = React.useState();

  useEffect(() => {
    const getData = async () => {
      const response = await axios.get("http://localhost:5000/all/geo_json_data");
      setData(response.data);
    };
    getData();
  },[]);

  if (data) {
    return <GeoJSON data={data} />;
  } else {
      return null;
    }
};

function Casual(props) {

  return (

    <div>
      <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
      <TemporaryDrawer/>
      <TileLayer
       attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <RetrieveData/>
      </MapContainer>
    </div>

  );
};

export default Casual;

