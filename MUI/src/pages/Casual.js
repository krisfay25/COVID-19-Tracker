import { useEffect, useCallback, useState } from 'react';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet'
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';
import Legend from '../components/Legend';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

function Casual(props) {
  // boolean for when polygonCoor has been populated and is ready to render
  const [ready, setReady] = useState(false);
  // this is where all of the values for the polygons will be kept
  const [polygonCoor, setPolygonCoor] = useState([]);

  const [legendDataType, setLegendDataType] = useState("cases");

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
  const setCoor = useCallback((coor, data) => {

    let polygons = [
      { "id": 44001, "color": "#ffffff", "coordinates": coor[0].geometry.coordinates, "cases": "" },
      { "id": 44003, "color": "#ffffff", "coordinates": coor[1].geometry.coordinates, "cases": "" },
      { "id": 44005, "color": "#ffffff", "coordinates": coor[2].geometry.coordinates, "cases": "" },
      { "id": 44007, "color": "#ffffff", "coordinates": coor[3].geometry.coordinates, "cases": "" },
      { "id": 44009, "color": "#ffffff", "coordinates": coor[4].geometry.coordinates, "cases": "" },
    ];

    for (let currData of data) {
      for (let currPoly of polygons) {
        if (currData.fips === currPoly.id) {

          if (legendDataType == "cases") {
            currPoly.cases = currData.total_cases;
            switch (true) {
              case (currPoly.cases >= 40000):
                currPoly.color = "#FF0000";
                break;
              case (currPoly.cases >= 30000):
                currPoly.color = "#FF5700";
                break;
              case (currPoly.cases >= 20000):
                currPoly.color = "#FFE400";
                break;
              case (currPoly.cases >= 10000):
                currPoly.color = "#6AFF00";
                break;
              case (currPoly.cases >= 0):
                currPoly.color = "#00FF00";
                break;
              default:
                currPoly.color = "#ffffff";
                break;
            }
          }
          else if (legendDataType == "vaccinations") {
            currPoly.cases = currData.total_cases;
            switch (true) {
              case (currPoly.cases >= 40000):
                currPoly.color = "#FF0000";
                break;
              case (currPoly.cases >= 30000):
                currPoly.color = "#FF5700";
                break;
              case (currPoly.cases >= 20000):
                currPoly.color = "#FFE400";
                break;
              case (currPoly.cases >= 10000):
                currPoly.color = "#6AFF00";
                break;
              case (currPoly.cases >= 0):
                currPoly.color = "#00FF00";
                break;
              default:
                currPoly.color = "#ffffff";
                break;
            }
          }
          else if (legendDataType == "deaths") {
            currPoly.cases = currData.total_cases;
            switch (true) {
              case (currPoly.cases >= 40000):
                currPoly.color = "#FF0000";
                break;
              case (currPoly.cases >= 30000):
                currPoly.color = "#FF5700";
                break;
              case (currPoly.cases >= 20000):
                currPoly.color = "#FFE400";
                break;
              case (currPoly.cases >= 10000):
                currPoly.color = "#6AFF00";
                break;
              case (currPoly.cases >= 0):
                currPoly.color = "#00FF00";
                break;
              default:
                currPoly.color = "#ffffff";
                break;
            }
          }
        }
      }
    }
    setPolygonCoor(polygons);
  }, []);

  useEffect(() => {
    async function getCoor() {
      const responses = await axios.get("http://localhost:5000/all/geo_json_data");
      swapCoor(responses.data);

      // Load county data
      const counties = [44001, 44003, 44005, 44007, 44009]
      Promise.all(counties.map(fips =>
        fetch(`http://localhost:5000/county/${fips}`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        })
          .then(response => response.json())
      )).then(data => {
        setCoor(responses.data, data);
        setReady(true);
      });
    };

    getCoor();
  }, [setCoor, swapCoor]);

  return (
    <div>
      {ready
        ? <MapContainer center={[41.700, -71.500]} zoom={10} scrollWheelZoom={true}>
          <TemporaryDrawer />
          <Stack spacing={0} direction="column" sx={{
            position: "absolute",
            maxWidth: 180,
            bottom: 5,
            left: 5,
          }}>
            <Button variant="contained" size="small" onClick={() => { setLegendDataType("cases") }}>Total Cases</Button>
            <Button variant="contained" size="small" onClick={() => { setLegendDataType("vaccinations") }}>Total Vaccinations</Button>
            <Button variant="contained" size="small" onClick={() => { setLegendDataType("deaths") }}>Total Deaths</Button>
          </Stack>
          <Legend dataType={legendDataType} />
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