import { useEffect, useCallback, useState } from 'react';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet'
import React, { Component } from 'react';
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';
import Legend from '../components/Legend';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import styled from "styled-components";
import CanvasJSReact from '../canvasjs.react';

var CanvasJSChart = CanvasJSReact.CanvasJSChart;

function Casual(props) {
  // boolean for when polygonCoor has been populated and is ready to render
  const [ready, setReady] = useState(false);
  // this is where all of the values for the polygons will be kept
  const [polygonCoor, setPolygonCoor] = useState([]);
  const [legendDataType, setLegendDataType] = useState("cases");

  const [counties] = useState([44001, 44003, 44005, 44007, 44009]);

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

  // sets the polygonCoor with the data fetched from the backend
  // new parameters can be added here
  const setCoor = useCallback((coor, data) => {

    let polygons = counties.map((fips, index) => {
      let currData = data[index];
      return {
        id: fips,
        coordinates: coor[index].geometry.coordinates,
        cases: currData.total_cases,
        county_name: currData.county_name,
        total_deaths: currData.total_deaths,
        total_hospital: currData.total_hospital,
        total_vaccinated: currData.total_vaccinated,
        case_rate: currData.case_rate_per_100k,
        vaccination_rate: currData.vaccinated_rate_per_100k,
        death_rate: currData.death_rate_per_100k,
        options: {
          title: {
            text: `Covid-19 Data For: ${currData.county_name}`
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: currData.total_cases },
              { label: "Total Vaccination", y: currData.total_vaccinated },
              { label: "Total Hospitalized", y: currData.total_hospital },
              { label: "Total Deaths", y: currData.total_deaths }
            ]
          }]
        }
      }
    });

    setPolygonCoor(polygons);
  }, [counties]);

  // Sets the colors of the polygons based on the current legend
  const polygonColor = (currPoly) => {
    if (legendDataType === "cases") {
      switch (true) {
        case (currPoly.case_rate >= 16000):
          return "#FF0000";
        case (currPoly.case_rate >= 12000):
          return "#FF5700";
        case (currPoly.case_rate >= 8000):
          return "#FFE400";
        case (currPoly.case_rate >= 4000):
          return "#6AFF00";
        case (currPoly.case_rate >= 0):
          return "#00FF00";
        default:
          return "#ffffff";
      }
    }
    else if (legendDataType === "vaccinations") {
      switch (true) {
        case (currPoly.vaccination_rate >= 800):
          return "#FF0000";
        case (currPoly.vaccination_rate >= 600):
          return "#FF5700";
        case (currPoly.vaccination_rate >= 400):
          return "#FFE400";
        case (currPoly.vaccination_rate >= 200):
          return "#6AFF00";
        case (currPoly.vaccination_rate >= 0):
          return "#00FF00";
        default:
          return "#ffffff";
      }
    }
    else if (legendDataType === "deaths") {
      switch (true) {
        case (currPoly.death_rate >= 400):
          return "#FF0000";
        case (currPoly.death_rate >= 350):
          return "#FF5700";
        case (currPoly.death_rate >= 200):
          return "#FFE400";
        case (currPoly.death_rate >= 100):
          return "#6AFF00";
        case (currPoly.death_rate >= 0):
          return "#00FF00";
        default:
          return "#ffffff";
      }
    }
  }

  useEffect(() => {
    async function getCoor() {
      const responses = await axios.get("http://localhost:5000/all/geo_json_data");
      swapCoor(responses.data);

      // Load county data
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
  }, [counties, setCoor, swapCoor]);

  //Style the pop-up in map
  const StyledPop = styled(Popup)`
width: 70vh;
border-radius: 0;

.leaflet-popup-content-wrapper {
  border-radius: 0;
}

.leaflet-popup-tip-container {
  visibility: hidden;
}
`;

  return (
    <div>
      {ready
        ? <MapContainer center={[41.550, -71.500]} zoom={9.5} scrollWheelZoom={true}>
          <TemporaryDrawer />
          <Stack spacing={0} direction="column" sx={{
            position: "absolute",
            maxWidth: 180,
            bottom: 5,
            left: 5,
          }}>
            <Button variant="contained" size="small" onClick={() => {
              setLegendDataType("cases");
            }}>Case Rate</Button>
            <Button variant="contained" size="small" onClick={() => {
              setLegendDataType("vaccinations");
            }}>Vaccination Rate</Button>
            <Button variant="contained" size="small" onClick={() => {
              setLegendDataType("deaths");
            }}>Death Rate</Button>
          </Stack>
          <Legend dataType={legendDataType} />
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {polygonCoor
            ? polygonCoor.map((coor) => (
              <Polygon positions={coor.coordinates} pathOptions={{ color:polygonColor(coor) }} key={coor.id}>
                <StyledPop>
                  <h2> {coor.county_name} </h2>
                  Case Rate: {coor.case_rate} <br></br>
                  Vaccination Rate: {coor.vaccination_rate} <br></br>
                  Death Rate: {coor.death_rate} <br></br>
                  Number of cases: {coor.cases} <br></br>
                  Total Vaccinated: {coor.total_vaccinated} <br></br>
                  Total Hospitalized: {coor.total_hospital} <br></br>
                  Total Deaths: {coor.total_deaths}
                  <br></br>
                  <br></br>
                  Pick a graph to visualize:
                  <br></br>
                  {/* -------------------- */}
                  <div class="dropdown">
                    <button class="dropbtn">Select Graph</button>
                    <div class="dropdown-content">
                      <a class="myDIV">Case Rates</a>
                      <div class="hide"> <CanvasJSChart options={coor.options} /> </div>
                      <a href="#">Vaccination Rates</a>
                      <a href="#">Death Rates</a>
                      <a href="#">Total Number of Cases</a>
                      <a href="#">Total Vaccinated</a>
                      <a href="#">Total Hospitalized</a>
                      <a href="#">Total Deaths</a>
                    </div>
                  </div>

                  {/* <CanvasJSChart options={coor.options} /> */}
                </StyledPop>
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