import { FunctionField, RaRecord, Datagrid, List, TextField, Create, Edit, Show, SimpleShowLayout, SimpleForm, TextInput } from 'react-admin';

export const StructureList = () => (
    <List exporter={false}>
        <Datagrid rowClick="edit">
            <TextField sortable={false} source="id" />
            <TextField source="name" />
            <FunctionField 
                source="structure"
                render={(record: RaRecord) =>
                    record?.structure
                        ? JSON.stringify(record.structure, null, 2)
                        : ''
                }
            />
            <TextField source="created_at" label="Created"/>
        </Datagrid>
    </List>
);

export const StructureCreate = () => (
    <Create>
        <SimpleForm>
            <TextInput source="name" />
            <TextInput 
                source="structure" 
                multiline 
                resettable
                minRows={5}
                parse={(value) => {
                    try {
                        return typeof value === 'string' ? JSON.parse(value) : value;
                    } catch (e) {
                        console.log(e);
                        return value;
                    }
                }}
                format={(value) => {
                    try {
                        return typeof value === 'object' ? JSON.stringify(value, null, 2) : value;
                    } catch (e) {
                        console.log(e);
                        return value;
                    }
                }}
            />
        </SimpleForm>
    </Create>
);

export const StructureEdit = () => (
    <Edit>
        <SimpleForm>
            <TextInput source="id" disabled />

            <TextInput source="name" />
            <TextInput 
                source="structure" 
                multiline 
                resettable
                minRows={5}
                parse={(value) => {
                    try {
                        return typeof value === 'string' ? JSON.parse(value) : value;
                    } catch (e) {
                        console.log(e);
                        return value;
                    }
                }}
                format={(value) => {
                    try {
                        return typeof value === 'object' ? JSON.stringify(value, null, 2) : value;
                    } catch (e) {
                        console.log(e);
                        return value;
                    }
                }}
            />
        </SimpleForm>
    </Edit>
);


export const StructureShow = () => (
    <Show>
        <SimpleShowLayout>
            <TextField source="id" />
            <TextField source="name" />
            <FunctionField
                source="structure"
                render={(record: RaRecord) =>
                    record?.structure
                        ? JSON.stringify(record.structure, null, 2)
                        : ''
                }
            />
        </SimpleShowLayout>
    </Show>
);