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
import SlidingPanel from 'react-sliding-side-panel';

var CanvasJSChart = CanvasJSReact.CanvasJSChart;

function Casual(props) {
  // boolean for when polygonCoor has been populated and is ready to render
  const [ready, setReady] = useState(false);
  // this is where all of the values for the polygons will be kept
  const [polygonCoor, setPolygonCoor] = useState([]);
  //this where the data will be stored within the graphs
  const [dataGraph, setDataGraph] = useState([]);
  const [legendDataType, setLegendDataType] = useState("cases");
  //this is the side panel that will hold graphs and county data
  const [openPanel, setOpenPanel] = useState(false);

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
  
  const setGraph = useCallback((graph_, data) => {
    let graphs = [
      {
        "case_rates":
        {
          title: {
            text: "Case Rates"
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" }
            ]
          }]
        }
      },
      {
        "vaccination_rates":
        {
          title: {
            text: "Vaccination Rates"
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" }
            ]
          }]
        }
      },
      {
        "death_rates":
        {
          title: {
            text: "Death Rates"
          },
          data: [{
            type: "column",
            dataPoints: [
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" },
              { label: "", y: "" }
            ]
          }]
        }
      }
    ]

    for (let currData of data) {
      for (let currGraphs of graphs) {

        //Case Rates Section
        if (currGraphs.case_rates) {
          if (currData.fips === 44001) {
            currGraphs.case_rates.data[0].dataPoints[0].label = currData.county_name;
            currGraphs.case_rates.data[0].dataPoints[0].y = currData.case_rate_per_100k;
          }
          if (currData.fips === 44003) {
            currGraphs.case_rates.data[0].dataPoints[1].label = currData.county_name;
            currGraphs.case_rates.data[0].dataPoints[1].y = currData.case_rate_per_100k;
          }
          if (currData.fips === 44005) {
            currGraphs.case_rates.data[0].dataPoints[2].label = currData.county_name;
            currGraphs.case_rates.data[0].dataPoints[2].y = currData.case_rate_per_100k;
          }
          if (currData.fips === 44007) {
            currGraphs.case_rates.data[0].dataPoints[3].label = currData.county_name;
            currGraphs.case_rates.data[0].dataPoints[3].y = currData.case_rate_per_100k;
          }
          if (currData.fips === 44009) {
            currGraphs.case_rates.data[0].dataPoints[4].label = currData.county_name;
            currGraphs.case_rates.data[0].dataPoints[4].y = currData.case_rate_per_100k;
          }
        }

        //Vaccination Rate section
        if (currGraphs.vaccination_rates) {
          if (currData.fips === 44001) {
            currGraphs.vaccination_rates.data[0].dataPoints[0].label = currData.county_name;
            currGraphs.vaccination_rates.data[0].dataPoints[0].y = currData.vaccinated_rate_per_100k;
          }
          if (currData.fips === 44003) {
            currGraphs.vaccination_rates.data[0].dataPoints[1].label = currData.county_name;
            currGraphs.vaccination_rates.data[0].dataPoints[1].y = currData.vaccinated_rate_per_100k;
          }
          if (currData.fips === 44005) {
            currGraphs.vaccination_rates.data[0].dataPoints[2].label = currData.county_name;
            currGraphs.vaccination_rates.data[0].dataPoints[2].y = currData.vaccinated_rate_per_100k;
          }
          if (currData.fips === 44007) {
            currGraphs.vaccination_rates.data[0].dataPoints[3].label = currData.county_name;
            currGraphs.vaccination_rates.data[0].dataPoints[3].y = currData.vaccinated_rate_per_100k;
          }
          if (currData.fips === 44009) {
            currGraphs.vaccination_rates.data[0].dataPoints[4].label = currData.county_name;
            currGraphs.vaccination_rates.data[0].dataPoints[4].y = currData.vaccinated_rate_per_100k;
          }
        }

        //Death Rates Section
        console.log("Death Rates");
        if (currGraphs.death_rates) {
          if (currData.fips === 44001) {
            currGraphs.death_rates.data[0].dataPoints[0].label = currData.county_name;
            currGraphs.death_rates.data[0].dataPoints[0].y = currData.death_rate_per_100k;
          }
          if (currData.fips === 44003) {
            currGraphs.death_rates.data[0].dataPoints[1].label = currData.county_name;
            currGraphs.death_rates.data[0].dataPoints[1].y = currData.death_rate_per_100k;
          }
          if (currData.fips === 44005) {
            currGraphs.death_rates.data[0].dataPoints[2].label = currData.county_name;
            currGraphs.death_rates.data[0].dataPoints[2].y = currData.death_rate_per_100k;
          }
          if (currData.fips === 44007) {
            currGraphs.death_rates.data[0].dataPoints[3].label = currData.county_name;
            currGraphs.death_rates.data[0].dataPoints[3].y = currData.death_rate_per_100k;
          }
          if (currData.fips === 44009) {
            currGraphs.death_rates.data[0].dataPoints[4].label = currData.county_name;
            currGraphs.death_rates.data[0].dataPoints[4].y = currData.death_rate_per_100k;
          }
        }
      }
    }
    setDataGraph(graphs);
  })
  
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
        case (currPoly.vaccination_rate >= 70000):
          return "#00FF00";
        case (currPoly.vaccination_rate >= 67500):
          return "#6AFF00";
        case (currPoly.vaccination_rate >= 65000):
          return "#FFE400";
        case (currPoly.vaccination_rate >= 62500):
          return "#FF5700";
        case (currPoly.vaccination_rate >= 60000):
          return "#FF0000";
        default:
          return "#ffffff";
      }
    }
    else if (legendDataType === "deaths") {
      console.log(currPoly.death_rate);
      switch (true) {  
        case (currPoly.death_rate >= 400):
          return "#FF0000";
        case (currPoly.death_rate >= 300):
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
        setGraph(responses.data, data);
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
                  Note: Rates are given per 100,000 population.
                  <br></br>
                  <br></br>
                  {legendDataType == "cases"
                    ? <div class="rates">Case Rate: {coor.case_rate} <br></br></div>
                    : <>Case Rate: {coor.case_rate} <br></br></>}

                  {legendDataType == "vaccinations"
                    ? <div class="rates"> Vaccination Rate: {coor.vaccination_rate}<br></br></div>
                    : <> Vaccination Rate: {coor.vaccination_rate} <br></br></>}

                  {legendDataType == "deaths"
                    ? <div class="rates"> Death Rate: {coor.death_rate} <br></br></div>
                    : <> Death Rate: {coor.death_rate} <br></br></>}

                  Number of cases: {coor.cases} <br></br>
                  Total Vaccinated: {coor.total_vaccinated} <br></br>
                  Total Hospitalized: {coor.total_hospital} <br></br>
                  Total Deaths: {coor.total_deaths}<br></br>
                  <br></br>
                  <h3>Click "Open" to visualize rates compared to other counties in graph format.</h3>
                  <button class="square_btn" onClick={() => setOpenPanel(true)}>Open</button>
                  <br></br>
                </StyledPop>

                <SlidingPanel
                  type={'left'}
                  isOpen={openPanel}
                  size={35}
                >
                  <div>
                    <button class="btn_position" onClick={() => setOpenPanel(false)}>close</button>
                    <div>
                      {legendDataType == "cases"
                        ? <CanvasJSChart options={dataGraph[0].case_rates} />
                        : <></>}

                      {legendDataType == "vaccinations"
                        ? <CanvasJSChart options={dataGraph[1].vaccination_rates} />
                        : <></>}

                      {legendDataType == "deaths"
                        ? <CanvasJSChart options={dataGraph[2].death_rates} />
                        : <></>}
                    </div>
                  </div>
                </SlidingPanel>

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