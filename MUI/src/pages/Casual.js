import React, { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Polygon, GeoJSON, Popup } from 'react-leaflet'
import * as L from 'leaflet';
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';

function Casual(props) {
  // holds the data fetched for the backend
  const [data, setData] = React.useState();
  // boolean for when the data has been loaded and populated
  const [loading, setLoading] = React.useState(false);
  // boolean for when polygonCoor has been populated and is ready to render
  const [ready, setReady] = React.useState(false);
  // this is where all of the values for the polygons will be kept
  const [polygonCoor, setPolygon] = React.useState();

  // originally, the coordinates are in the wrong format. 
  // makes coordinates [x,y] => [y,x]
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

  // sets the polygonCoor with the data fetched from the backend. also sets id and color
  // new parameters can be added here
  const setCoor = async () => {
    const response = await 
    setPolygon([{"id": "001", "color": "red", "coordinates": data[0].geometry.coordinates},
      {"id": "003", "color": "blue", "coordinates": data[1].geometry.coordinates},
      {"id": "005", "color": "green", "coordinates": data[2].geometry.coordinates},
      {"id": "007", "color": "yellow", "coordinates": data[3].geometry.coordinates},
      {"id": "009", "color": "purple", "coordinates": data[4].geometry.coordinates},
    ]);

    // TODO :run into a problem here. when swapCoor is called, polygonCoor 
    // should be populated but isn't, which throws an error. I tried adding a loop to 
    // keep running until polygonCoor has something in it, but it doesnt happen and 
    // its an infinite loop
    var temp = false;
    while(!temp){
      temp = swapCoor();
    }
  }
  
  // gets the data from the backend
  const getData = async () => {
    const response = await axios.get("http://localhost:5000/all/geo_json_data");
    setData(response.data);
    setLoading(true);
  };  

  if(!loading){
    getData();
  }

  useEffect(() => {
    
    // if the data is loaded, populate polygonCoor and set ready into true
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
      ))
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

