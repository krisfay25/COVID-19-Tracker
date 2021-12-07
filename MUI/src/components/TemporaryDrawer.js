import { useState } from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DoubleButton from './DoubleButton';
import SettingsIcon from '@mui/icons-material/Settings';
import './TemporaryDrawer.css';
import { GraphSwitch } from './GraphSwitch';
import { MapSwitch } from './MapSwitch';

export default function TemporaryDrawer() {
  const [open, setOpen] = useState(false);

  const toggleDrawer = (isOpen) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setOpen(isOpen);
  };

  const list = () => (
    <Box
      sx={{ width: 400 }}
      role="presentation"
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {['Switch View','Toggle Graphs', 'Toggle Maps'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemText primary={text} />
            <ListItemIcon>
              {index === 0 ?  <DoubleButton/>
                : (index === 1 ? <GraphSwitch/> : <MapSwitch/>)}
            </ListItemIcon>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <div>
      <Button onClick={toggleDrawer(true)}><SettingsIcon sx={{color: 'black'}} fontSize="large"/></Button>
      <Drawer
        anchor="left"
        open={open}
        onClose={toggleDrawer(false)}
      >
        {list()}
      </Drawer>
    </div>
  );
}
