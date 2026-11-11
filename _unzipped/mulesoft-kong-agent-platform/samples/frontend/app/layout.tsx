import type { ReactNode } from 'react';
export default function RootLayout({children}:{children:ReactNode}) { return <html lang="ja"><body style={{fontFamily:'sans-serif',maxWidth:920,margin:'48px auto',padding:20}}>{children}</body></html>; }
