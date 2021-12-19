import React from 'react'
import { useState } from 'react';
import { Button, Typography, CssBaseline } from '@material-ui/core';
import Stack from '@mui/material/Stack';
import { Link } from 'react-router-dom';
import './mainPageStyle/main.css'
import { makeStyles } from "@material-ui/core/styles";
import { fontWeight, letterSpacing } from '@mui/system';

const useStyles = makeStyles({
  custom: {
    color: "#FFFFFF",
    letterSpacing: 20
  },
  custom2:{
    color: "#FFFFFF",
    fontFamily: "New Century Schoolbook, TeX Gyre Schola, serif",
    letterSpacing: 15
  },
  custom3:{
    backgroundColor: "#ffffff",
    width: "1000px",
    marginLeft: "auto",
    marginRight: "auto",
    borderRadius: "45px 200px 70px 200px",
    color: "black"
  }
});

function Main(props) {
  const [isShownCasual, setIsShownCasual] = useState(false);
  const [isShownInformative, setIsShownInformative] = useState(false);
  const classes = useStyles();

  return (
    <>
      <CssBaseline />

      <main class="bg_image">
        <div>
          <br />
          <Typography variant='h2' className={classes.custom} align="center" color="textPrimary" gutterBottom>
            Covid-19 Rhode Island Tracker
            <hr color='#fffff' width='1200px' size='30px'></hr>
          </Typography>


          <Typography variant='h4' className={classes.custom2} align="center" color="textSecondary" gutterBottom>
            Choose your view:
          </Typography>
          <br />
          <br />
          <br />
          <br />

          <Stack direction="row" spacing={10} style={{ justifyContent: 'center' }}>
            <Link to="/Casual" style={{ textDecoration: 'none' }}>
              <Button
                variant="contained" size="large"
                onMouseEnter={() => setIsShownCasual(true)}
                onMouseLeave={() => setIsShownCasual(false)}>
                Casual
              </Button>
            </Link>
            <Link to="/Informative" style={{ textDecoration: 'none' }}>
              <Button
                variant="contained" size="large"
                onMouseEnter={() => setIsShownInformative(true)}
                onMouseLeave={() => setIsShownInformative(false)}>
                Informative
              </Button>
            </Link>


          </Stack>
          {isShownCasual && (

            <div>
              <br />
              <Typography variant='h5' className={classes.custom3} align="center" color="textSecondary" gutterBottom>
                This selection allows visual aids in the form of maps and gives a
                <br />county by county breakdown of COVID cases, vaccination rates and more.
              </Typography>
            </div>
          )}

          {isShownInformative && (

            <div>
              <br />
              <Typography variant='h5' className={classes.custom3} align="center" color="textSecondary" gutterBottom>
                This selection allows the user to access more detailed data in a spreadsheet
                <br />form without the map.
              </Typography>
            </div>
          )}
        </div>
      </main>
    </>
  );
}

export default Main;

