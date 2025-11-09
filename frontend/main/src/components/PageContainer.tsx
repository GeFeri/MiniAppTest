import type {ReactNode} from "react";

export const PageContainer = ({ children }: { children: ReactNode }) => (
  <div className="pt-[64px] pb-16 px-3 min-h-screen w-full bg-gray-50">
    {children}
  </div>
);