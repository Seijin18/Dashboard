"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, Dumbbell, Calendar, LogIn } from "lucide-react";

const links = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/pessoas", label: "Pessoas", icon: Users },
  { href: "/modalidades", label: "Modalidades", icon: Dumbbell },
  { href: "/turmas", label: "Turmas", icon: Calendar },
  { href: "/login", label: "Login", icon: LogIn },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="bg-slate-900 text-white px-6 py-3 flex items-center gap-6 shadow-md">
      <span className="font-bold text-lg tracking-tight">Kannon Do</span>
      <div className="flex gap-1 flex-wrap">
        {links.map(({ href, label, icon: Icon }) => {
          const active = pathname === href || (href !== "/" && pathname.startsWith(href));
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm transition-colors ${
                active ? "bg-slate-700 text-white" : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
