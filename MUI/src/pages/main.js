import React from 'react'
import { useState } from 'react';
import { Button, Typography, AppBar, Car, CardActions, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container } from '@material-ui/core';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import Stack from '@mui/material/Stack';
import ButtonBase from '@mui/material/ButtonBase';
import {Link} from 'react-router-dom';

function Main(props) {
    const [isShownCasual, setIsShownCasual] = useState(false);
    const [isShownInformative, setIsShownInformative] = useState(false);
    return (
      <>
        <CssBaseline />
        <AppBar position="relative">
          <Toolbar>
            <MedicalServicesIcon />
            <Typography variant="h6">
              Home
            </Typography>
          </Toolbar>
        </AppBar>
  
        <main>
          <div>
            <br/>
            <Typography variant='h2' align="center" color="textPrimary" gutterBottom>
              Covid Tracker
            </Typography>
  
            <Typography variant='h5' align="center" color="textSecondary" gutterBottom>
              Choose your view:
            </Typography>
            <br/>
            <br/>
            <br/>
            <br/>
  
            <Stack direction="row" spacing={10} style={{justifyContent: 'center'}}>
              <Link to="/Casual">
                  <Button 
                  variant="contained" size="large"
                  onMouseEnter={() => setIsShownCasual(true)}
                  onMouseLeave={() => setIsShownCasual(false)}>
                      Casual
                </Button>
              </Link>
              <Link to="/Informative">
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
                  <Typography variant='h5' align="center" color="textSecondary" gutterBottom>
                  Casual: 
                  <br/>This selection allows visual aids in the form of maps and give a 
                  <br/>county by county breakdown of COVID cases and vaccination rates.
                  </Typography>
                </div>
              )}
  
              {isShownInformative && (
                
                <div>
                  <br />
                   <Typography variant='h5' align="center" color="textSecondary" gutterBottom>
                  Informative: 
                  <br/>This selection allows the user to access more detailed data in a spreadsheet 
                  <br/>form without the map.
                  </Typography>
                </div>
              )}
          </div>
        </main>
      </>
    );
}

export default Main;

