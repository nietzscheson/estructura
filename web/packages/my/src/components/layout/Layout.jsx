// src/components/layout/CustomLayout.tsx
import { Layout } from 'react-admin';
import CustomAppBar from './AppBar';
// import { CustomSidebar } from './SideBar';
import { CustomMenu } from "./CustomMenu";


const CustomLayout = props => (
  <Layout {...props} appBar={CustomAppBar}/>
);

export default CustomLayout;
