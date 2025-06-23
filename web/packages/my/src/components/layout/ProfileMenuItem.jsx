import React from 'react';
import { MenuItemLink } from 'react-admin';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const ProfileMenuItem = () => (
  <MenuItemLink
    to="/profile" // Make sure this path matches your routing setup for the profile page
    primaryText="Profile"
    leftIcon={<AccountCircleIcon />}
  />
);

export default ProfileMenuItem;