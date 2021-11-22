import React, { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Polygon, GeoJSON, Popup } from 'react-leaflet'
import * as L from 'leaflet';
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';

function Casual(props) {
  const [data, setData] = React.useState();
  const [loading, setLoading] = React.useState(false);
  const [ready, setReady] = React.useState(false);
  const [polygonCoor, setPolygon] = React.useState();

  const swapCoor = () => {
    if (!polygonCoor){
      return false;
    }
    var temp;
    polygonCoor[0].coordinates.forEach(item => {
      temp = item[0];
      item[0] = item[1];
      item[1] = temp;
    });
  
    polygonCoor[1].coordinates.forEach(item => {
      temp = item[0];
      item[0] = item[1];
      item[1] = temp;
    });
  
    polygonCoor[3].coordinates.forEach(item => {
      temp = item[0];
      item[0] = item[1];
      item[1] = temp;
    });
  
    for(let i = 0 ; i < polygonCoor[2].coordinates.length; i++){
        polygonCoor[2].coordinates[i][0].forEach(item => {
        temp = item[0];
        item[0] = item[1];
        item[1] = temp;
      });
    }
    for(let i = 0 ; i < polygonCoor[4].coordinates.length; i++){
        polygonCoor[4].coordinates[i][0].forEach(item => {
          temp = item[0];
          item[0] = item[1];
          item[1] = temp;
        });
      }
    return true;
  }

  const setCoor = async () => {
    const response = await 
    setPolygon([{"id": "001", "color": "red", "coordinates": data[0].geometry.coordinates},
      {"id": "003", "color": "blue", "coordinates": data[1].geometry.coordinates},
      {"id": "005", "color": "green", "coordinates": data[2].geometry.coordinates},
      {"id": "007", "color": "yellow", "coordinates": data[3].geometry.coordinates},
      {"id": "009", "color": "purple", "coordinates": data[4].geometry.coordinates},
    ]);
    var temp = false;
    while(!temp){
      swapCoor();
    }
  }
  
  const getData = async () => {
    const response = await axios.get("http://localhost:5000/all/geo_json_data");
    setData(response.data);
    setLoading(true);
  };  

  if(!loading){
    getData();
  }

  useEffect(() => {

    if(loading){
      setCoor();
      setReady(true);
    }
  },[loading]);

  return (
    <div>
    {ready ? 
     <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
      <TemporaryDrawer/>
      <TileLayer
       attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {polygonCoor ?
      polygonCoor.map((coor) => (
        <Polygon positions={coor.coordinates} color={coor.color} >
          <Popup>
            {coor.id}
          </Popup>
        </Polygon>
      )
      )
      :
      <></>}
      </MapContainer>
      :
      <>Loading....</>
    }
     
    </div>

  );
};

export default Casual;

