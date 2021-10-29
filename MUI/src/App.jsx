import React from 'react'
import { useState } from 'react';
import { Button, Typography, AppBar, Car, CardActions, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container } from '@material-ui/core';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import Stack from '@mui/material/Stack';
import ButtonBase from '@mui/material/ButtonBase';
import Main from './pages/main';
import Casual from './pages/Casual';
import Informative from './pages/Informative';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

const App = () => {
  const [isShownCasual, setIsShownCasual] = useState(false);
  const [isShownInformative, setIsShownInformative] = useState(false);
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Main} />
          <Route path="/casual" component={Casual} />
          <Route path="/informative" component={Informative} />
        </Switch>
      </div>
    </Router>
  )
}
export default App;
