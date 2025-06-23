import {
    Datagrid,
    List,
    TextField,
    Create,
    Show,
    SimpleShowLayout,
    SimpleForm,
    ReferenceInput,
    SelectInput,
    FileInput,
    FileField,
    ReferenceField,
    ArrayField,
    FunctionField,
} from 'react-admin';
import { FilePreview } from './FilePreview';
import { Box, Typography, Stack, IconButton, Tooltip } from "@mui/material";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import { useState } from "react";
import { useEffect } from 'react';
import { useRefresh } from 'react-admin';


export const DocumentsList = () => (
    <List exporter={false}>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField source="structure_id" reference="structures" link="show" />
            <TextField source="status" label="Status"/>
            <TextField source="created_at" label="Created"/>

        </Datagrid>
    </List>
);

export const DocumentsCreate = () => (
    <Create>
        <SimpleForm>
            <ReferenceInput label="Structure" source="structure_id" reference="structures">
                <SelectInput optionText="name" />
            </ReferenceInput>
            <FileInput source="file" label="File" placeholder={<p>Drop your file here</p>} accept={{ 
                'application/pdf': ['.pdf'],
                'image/jpeg': ['.jpg', '.jpeg'],
                'image/png': ['.png']

            }}>
                <FileField source="file" title="title" />
            </FileInput>
        </SimpleForm>
    </Create>
);

const CopyableText = ({ text }: { text: string }) => {
    const [copied, setCopied] = useState(false);
  
    const copyToClipboard = () => {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1000);
    };
  
    return (
      <Box display="flex" alignItems="center" gap={1}>
        <Typography variant="body2" sx={{ wordBreak: "break-all" }}>
          {text}
        </Typography>
        <Tooltip title={copied ? "Copied!" : "Copy"}>
          <IconButton size="small" onClick={copyToClipboard}>
            <ContentCopyIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
    );
  };


  import { useRecordContext } from 'react-admin';
  import LinearProgress from '@mui/material/LinearProgress';
  
  const PageAnalysisBlock = () => {
    const record = useRecordContext();
    const refresh = useRefresh();
  
    useEffect(() => {
      if (record?.status === 'processing') {
        const interval = setInterval(() => {
          refresh();
        }, 5000);
        return () => clearInterval(interval);
      }
    }, [record?.status, refresh]);
  
    if (!record) return null;
  
    const isProcessing = record.status === 'processing';
  
    return (
      <Box flex="1" overflow="auto" maxHeight="calc(100vh - 150px)" pr={2}>
        {isProcessing ? (
          <Box p={2}>
            <Typography variant="body2" gutterBottom>
              Analyzing pages...
            </Typography>
            <LinearProgress />
          </Box>
        ) : (
          <ArrayField source="pages">
            <Datagrid bulkActionButtons={false}>
              <TextField source="number" />
              <FunctionField
                label="Analysis"
                render={(page: { analysis?: unknown }) =>
                  page.analysis ? (
                    <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>
                      {JSON.stringify(page.analysis, null, 2)}
                    </pre>
                  ) : (
                    'No analysis'
                  )
                }
              />
            </Datagrid>
          </ArrayField>
        )}
      </Box>
    );
  };

  export const DocumentsShow = () => (
    <Show>
      <SimpleShowLayout>
        <Box display="flex" gap={4} alignItems="flex-start" width="100%" height="calc(100vh - 150px)">
          {/* Izquierda */}
          <Box flex="0 0 350px">
            <Stack spacing={2}>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  ID
                </Typography>
                <FunctionField render={(record) => <CopyableText text={record.id} />} />
              </Box>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  Status
                </Typography>
                <FunctionField render={(record) => <CopyableText text={record.status} />} />
              </Box>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  Workspace
                </Typography>
                <ReferenceField
                  source="workspace_id"
                  reference="workspaces"
                  link="show"
                />
              </Box>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  File
                </Typography>
                <Box display="flex" justifyContent="center" >
                    <FunctionField
                    render={(record) => <FilePreview src={record.file} />}
                    />
                </Box>
              </Box>
            </Stack>
          </Box>
  
          {/* Derecha */}
          <PageAnalysisBlock />

        </Box>
      </SimpleShowLayout>
    </Show>
  );