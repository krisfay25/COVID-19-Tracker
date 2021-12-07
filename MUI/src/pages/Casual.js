import { useEffect, useCallback, useState } from 'react';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet'
import './leaflet/Casual.css';
import TemporaryDrawer from '../components/TemporaryDrawer';
import axios from 'axios';
import Legend from '../components/Legend';
import styled from "styled-components";
import CanvasJSReact from '../canvasjs.react';

//var CanvasJSReact = require('./canvasjs.react');
var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
var options;

const StyledPop = styled(Popup)`
  width: 50vh;
  border-radius: 0;

  .leaflet-popup-content-wrapper {
    border-radius: 0;
  }

  .leaflet-popup-tip-container {
    visibility: hidden;
  }
`;

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
  const setCoor = useCallback((coor, data) => {

    let polygons = [
      {
        "id": 44001,
        "color": "#ffffff",
        "coordinates": coor[0].geometry.coordinates,
        "cases": "",
        "county_name": "",
        "total_deaths": "",
        "total_hospital": "",
        "total_vaccinated": "",
        "options":
        {
          title: {
            text: ""
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: "" },
              { label: "Total Vaccination", y: "" },
              { label: "Total Hospitalized", y: "" },
              { label: "Total Deaths", y: "" }
            ]
          }]
        }
      },
      {
        "id": 44003,
        "color": "#ffffff",
        "coordinates": coor[1].geometry.coordinates,
        "cases": "",
        "county_name": "",
        "total_deaths": "",
        "total_hospital": "",
        "total_vaccinated": "",
        "options":
        {
          title: {
            text: ""
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: "" },
              { label: "Total Vaccination", y: "" },
              { label: "Total Hospitalized", y: "" },
              { label: "Total Deaths", y: "" }
            ]
          }]
        }
      },
      {
        "id": 44005,
        "color": "#ffffff",
        "coordinates": coor[2].geometry.coordinates,
        "cases": "",
        "county_name": "",
        "total_deaths": "",
        "total_hospital": "",
        "total_vaccinated": "",
        "options":
        {
          title: {
            text: ""
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: "" },
              { label: "Total Vaccination", y: "" },
              { label: "Total Hospitalized", y: "" },
              { label: "Total Deaths", y: "" }
            ]
          }]
        }
      },
      {
        "id": 44007,
        "color": "#ffffff",
        "coordinates": coor[3].geometry.coordinates,
        "cases": "",
        "county_name": "",
        "total_deaths": "",
        "total_hospital": "",
        "total_vaccinated": "",
        "options":
        {
          title: {
            text: ""
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: "" },
              { label: "Total Vaccination", y: "" },
              { label: "Total Hospitalized", y: "" },
              { label: "Total Deaths", y: "" }
            ]
          }]
        }
      },
      {
        "id": 44009,
        "color": "#ffffff",
        "coordinates": coor[4].geometry.coordinates,
        "cases": "",
        "county_name": "",
        "total_deaths": "",
        "total_hospital": "",
        "total_vaccinated": "",
        "options":
        {
          title: {
            text: ""
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "Total Cases", y: "" },
              { label: "Total Vaccination", y: "" },
              { label: "Total Hospitalized", y: "" },
              { label: "Total Deaths", y: "" }
            ]
          }]
        }
      }
    ];

    console.log(polygons);

    for (let currData of data) {
      for (let currPoly of polygons) {
        if (currData.fips === currPoly.id) {
          currPoly.cases = currData.total_cases;
          currPoly.county_name = currData.county_name;
          currPoly.total_deaths = currData.total_deaths;
          currPoly.total_hospital = currData.total_hospital;
          currPoly.total_vaccinated = currData.total_vaccinated;

          //Setting graph data
          currPoly.options.title.text = "Covid-19 Data For: " + currData.county_name;
          currPoly.options.data[0].dataPoints[0].y = currData.total_cases;
          currPoly.options.data[0].dataPoints[1].y = currData.total_vaccinated;
          currPoly.options.data[0].dataPoints[2].y = currData.total_hospital;
          currPoly.options.data[0].dataPoints[3].y = currData.total_deaths; 

          switch (true) {
            case (currPoly.cases >= 40000):
              currPoly.color = "#990000";
              break;
            case (currPoly.cases >= 30000):
              currPoly.color = "#cc0000";
              break;
            case (currPoly.cases >= 20000):
              currPoly.color = "#ff0000";
              break;
            case (currPoly.cases >= 10000):
              currPoly.color = "#ff4d4d";
              break;
            default:
              currPoly.color = "#ffffff";
              break;
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
        ? <MapContainer center={[41.550, -71.500]} zoom={9.5} scrollWheelZoom={true}>
          <TemporaryDrawer />
          <Legend />
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {polygonCoor
            ? polygonCoor.map((coor) => (
              <Polygon positions={coor.coordinates} color={coor.color} key={coor.id}>
                <StyledPop>
                  <h2> {coor.county_name} </h2>
                  Number of cases: {coor.cases} <br></br>
                  Total Vaccinated: {coor.total_vaccinated} <br></br>
                  Total Hospitalized: {coor.total_hospital} <br></br>
                  Total Deaths: {coor.total_deaths}
                  <br></br>
                  <br></br>
                  <CanvasJSChart options={coor.options} />
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