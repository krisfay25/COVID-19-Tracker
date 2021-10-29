import React from 'react'
import Main from './pages/main';
import Casual from './pages/Casual';
import Informative from './pages/Informative';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

const App = () => {
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
