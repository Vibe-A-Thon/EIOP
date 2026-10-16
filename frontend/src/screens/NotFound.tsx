import { Link } from "react-router-dom";
import { Compass } from "lucide-react";
import { Button } from "../components/ui/Button";

export function NotFound() {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-4 p-8 text-center" data-testid="not-found">
      <div className="grid h-16 w-16 place-items-center rounded-full border border-[var(--border-subtle)] bg-[var(--bg-panel)] text-[var(--text-muted)]">
        <Compass size={28} />
      </div>
      <div>
        <p className="font-heading text-3xl font-bold tracking-tight">404</p>
        <p className="mt-1 text-sm text-[var(--text-muted)]">This screen doesn’t exist, or the resource was not found.</p>
      </div>
      <Link to="/overview">
        <Button variant="primary" data-testid="not-found-home">Back to Overview</Button>
      </Link>
    </div>
  );
}
