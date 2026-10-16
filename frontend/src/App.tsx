import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useAuth } from "./lib/auth";
import { AppShell } from "./shell/AppShell";
import { SignIn } from "./screens/SignIn";
import { Overview } from "./screens/Overview";
import { Ask } from "./screens/Ask";
import { GraphExplorer } from "./screens/GraphExplorer";
import { Entity360 } from "./screens/Entity360";
import { Schema } from "./screens/Schema";
import { IngestionConsole } from "./screens/IngestionConsole";

export default function App() {
  const { session } = useAuth();
  const location = useLocation();

  if (!session) {
    return (
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route
          path="*"
          element={<Navigate to="/signin" replace state={{ from: location.pathname }} />}
        />
      </Routes>
    );
  }

  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Navigate to="/overview" replace />} />
        <Route path="/overview" element={<Overview />} />
        <Route path="/ask" element={<Ask />} />
        <Route path="/graph" element={<GraphExplorer />} />
        <Route path="/entity/:id" element={<Entity360 />} />
        <Route path="/schema" element={<Schema />} />
        <Route path="/ingestion" element={<IngestionConsole />} />
        <Route path="/signin" element={<Navigate to="/overview" replace />} />
        <Route path="*" element={<Navigate to="/overview" replace />} />
      </Routes>
    </AppShell>
  );
}
