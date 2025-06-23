import { Dialog, DialogContent } from '@mui/material';
import { useState } from 'react';

export const ClickableImage = ({ src }: { src: string }) => {
    const [open, setOpen] = useState(false);

    return (
        <>
            <img
                src={src}
                alt="Preview"
                style={{ maxWidth: 200, cursor: 'pointer', borderRadius: 8 }}
                onClick={() => setOpen(true)}
            />
            <Dialog open={open} onClose={() => setOpen(false)} maxWidth="lg">
                <DialogContent>
                    <img
                        src={src}
                        alt="Full Preview"
                        style={{ width: '100%', maxHeight: '95vh', objectFit: 'contain' }}
                    />
                </DialogContent>
            </Dialog>
        </>
    );
};

export const FilePreview = ({ src, type }: { src: string; type?: string }) => {
    if (!src) return null;

    const isImage = /\.(png|jpe?g)$/i.test(src) || type?.startsWith('image/');
    const isPDF = /\.pdf$/i.test(src) || type === 'application/pdf';

    if (isImage) return <ClickableImage src={src} />;

    if (isPDF) {
        return (
            <embed
                src={src}
                type="application/pdf"
                width="100%"
                height="500px"
                style={{ border: "1px solid #ccc", borderRadius: 8 }}
            />
        );
    }

    return <span>Unsupported file type</span>;
};