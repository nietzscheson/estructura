//"use client";
import { Admin, Resource, defaultDarkTheme } from "react-admin";
import  DataProvider from "@/DataProvider";
import { StructureList, StructureCreate, StructureEdit, StructureShow} from "@/components/Structures";
import { DocumentsList, DocumentsCreate, DocumentsShow} from "@/components/Documents";
import { DataObject } from "@mui/icons-material";
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';
import { CustomLayout } from '@/components/layout';
import { authProvider } from "@/AuthProvider";

const AdminApp = () => (
  <Admin loginPage={false} layout={CustomLayout} theme={defaultDarkTheme} authProvider={authProvider} dataProvider={DataProvider} title="{ Estructura }">
    <Resource
      name="documents"
      list={DocumentsList}
      create={DocumentsCreate}
      show={DocumentsShow}
      recordRepresentation="name"
      icon={DocumentScannerIcon}
    />
    <Resource
      name="structures"
      list={StructureList}
      create={StructureCreate}
      edit={StructureEdit}
      show={StructureShow}
      recordRepresentation="name"
      icon={DataObject}
    />

  </Admin>
);

export default AdminApp;