/// <reference types="vite/client" />

declare module '@config' {
  const config: Record<string, unknown>;
  export default config;
}

declare module '*.yml' {
  const content: Record<string, unknown>;
  export default content;
}

// Match the named SVG export produced by vite-plugin-svgr.
declare module '*.svg' {
  import type { FC, SVGProps } from 'react';
  export const ReactComponent: FC<SVGProps<SVGSVGElement>>;
}
