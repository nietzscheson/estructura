// src/components/layout/CustomSidebar.tsx
import { Sidebar } from 'react-admin';
import { Box, } from '@mui/material';
import { AccountSummary } from './AccountSummary';

export const CustomSidebar = (props) => {
  return (
    <Sidebar {...props}>
      {props.children}
      <Box mt="auto" px={1.5} pb={1.5}>
        <AccountSummary />
      </Box>
    </Sidebar>
  );
};
