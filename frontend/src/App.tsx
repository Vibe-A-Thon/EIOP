import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useAuth } from "./lib/auth";
import { AppShell } from "./shell/AppShell";
import { SignIn } from "./screens/SignIn";
import { Overview } from "./screens/Overview";
import { Ask } from "./screens/Ask";
import { GraphExplorer } from "./screens/GraphExplorer";
import { MetaGraph } from "./screens/MetaGraph";
import { Entity360 } from "./screens/Entity360";
import { Schema } from "./screens/Schema";
import { IngestionConsole } from "./screens/IngestionConsole";
import { Impact } from "./screens/Impact";
import { Changes } from "./screens/Changes";
import { Incidents } from "./screens/Incidents";
import { Query } from "./screens/Query";
import { Ontology } from "./screens/Ontology";
import { Quality } from "./screens/Quality";
import { Agents } from "./screens/Agents";
import { Reports } from "./screens/Reports";
import { Snapshots } from "./screens/Snapshots";
import { Governance } from "./screens/Governance";
import { Tenant } from "./screens/Tenant";
import { Health } from "./screens/Health";
import { Settings } from "./screens/Settings";
import { Help } from "./screens/Help";
import { NotFound } from "./screens/NotFound";

export default function App() {
  const { session } = useAuth();
  const location = useLocation();

  if (!session) {
    return (
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="*" element={<Navigate to="/signin" replace state={{ from: location.pathname }} />} />
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
        <Route path="/meta-graph" element={<MetaGraph />} />
        <Route path="/entity/:id" element={<Entity360 />} />
        <Route path="/query" element={<Query />} />
        <Route path="/impact" element={<Impact />} />
        <Route path="/changes" element={<Changes />} />
        <Route path="/incidents" element={<Incidents />} />
        <Route path="/ontology" element={<Ontology />} />
        <Route path="/quality" element={<Quality />} />
        <Route path="/snapshots" element={<Snapshots />} />
        <Route path="/ingestion" element={<IngestionConsole />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/health" element={<Health />} />
        <Route path="/governance" element={<Governance />} />
        <Route path="/tenant" element={<Tenant />} />
        <Route path="/schema" element={<Schema />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/help" element={<Help />} />
        <Route path="/signin" element={<Navigate to="/overview" replace />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AppShell>
  );
}
