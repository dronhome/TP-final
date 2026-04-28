"use client";

import Image from "next/image";
import { useEffect, useState, MouseEvent } from "react";

// ─── Data ────────────────────────────────────────────────────────────────────

const DOCS = {
    // ── Zimný semester ───────────────────────────────────────────────────────
    minutes: [
        { label: "Zápisnica 1", href: "/docs/minutes/zapisnica 1.pdf" },
        { label: "Zápisnica 2", href: "/docs/minutes/zapisnica 2.pdf" },
        { label: "Zápisnica 3", href: "/docs/minutes/zapisnica 3.pdf" },
        { label: "Zápisnica 4", href: "/docs/minutes/zapisnica 4.pdf" },
        { label: "Zápisnica 5", href: "/docs/minutes/zapisnica 5.pdf" },
        { label: "Zápisnica 6", href: "/docs/minutes/zapisnica 6.pdf" },
        { label: "Zápisnica 7", href: "/docs/minutes/zapisnica 7.pdf" },
        { label: "Zápisnica 8", href: "/docs/minutes/zapisnica 8.pdf" },
        { label: "Zápisnica 9", href: "/docs/minutes/zapisnica 9.pdf" },
        { label: "Zápisnica 10", href: "/docs/minutes/zapisnica 10.pdf" },
    ],
    backlog: [
        { label: "Backlog report", href: "/docs/backlog/backlog-report.pdf" },
    ],
    retrospective: [
        { label: "Retrospektíva – Sprint 1", href: "/docs/retrospectives/Sprint_1.pdf" },
        { label: "Retrospektíva – Sprint 2", href: "/docs/retrospectives/Sprint_2.pdf" },
        { label: "Retrospektíva – Sprint 3", href: "/docs/retrospectives/Sprint_3.pdf" },
        { label: "Retrospektíva – Sprint 4", href: "/docs/retrospectives/Sprint_4.pdf" },
        { label: "Retrospektíva – Sprint 5", href: "/docs/retrospectives/Sprint_5.pdf" },
    ],
    // ── Letný semester ────────────────────────────────────────────────────────
    minutes_summer: [
        { label: "Zápisnica – Sprint 1", href: "/docs/minutes/letny/zapisnica sprint 1.pdf" },
        { label: "Zápisnica – Sprint 2", href: "/docs/minutes/letny/zapisnica sprint 2.pdf" },
        { label: "Zápisnica – Sprint 3", href: "/docs/minutes/letny/zapisnica sprint 3.pdf" },
        { label: "Zápisnica – Sprint 4", href: "/docs/minutes/letny/zapisnica sprint 4.pdf" },
        { label: "Zápisnica – Sprint 5", href: "/docs/minutes/letny/zapisnica sprint 5.pdf" },
    ],
    backlog_summer: [
        { label: "Backlog report", href: "/docs/backlog/letny/backlog-report.pdf" },
    ],
    retrospective_summer: [
        { label: "Retrospektíva – Sprint 1", href: "/docs/retrospectives/letny/Retrospektiva_Sprint1.pdf" },
        { label: "Retrospektíva – Sprint 2", href: "/docs/retrospectives/letny/Retrospektiva_Sprint2.pdf" },
        { label: "Retrospektíva – Sprint 3", href: "/docs/retrospectives/letny/Retrospektiva_Sprint3.pdf" },
        { label: "Retrospektíva – Sprint 4", href: "/docs/retrospectives/letny/Retrospektiva_Sprint4.pdf" },
        { label: "Retrospektíva – Sprint 5", href: "/docs/retrospectives/letny/Retrospektiva_Sprint5.pdf" },
    ] as { label: string; href: string }[],
    // ── Bez semestra ─────────────────────────────────────────────────────────
    methodologies: [
        { label: "Metodika komunikácie", href: "/docs/methodologies/Metodika-komunikácie.pdf " },
        { label: "Metodika revízie kódu", href: "/docs/methodologies/Metodika-revízieKódu.pdf" },
        { label: "Metodika spravovania backlogu", href: "/docs/methodologies/Metodika-spravovaniaBacklogu.pdf" },
        { label: "Metodika práce s robotom", href: "/docs/methodologies/Metodika-prácesRobotom.pdf" },
        { label: "Metodika spracovania videí", href: "/docs/methodologies/Metodika-spracovaniaVideí.pdf" },
    ],
};

const TEAM = [
    { name: "Andrii Kostiushko", role: "Projektový manažér, Robotik / Integrátor NAO robota (ruky)", img: "/photos/andrii_k.jpg" },
    { name: "Oleksandra Pozdniakova", role: "Frontend vývojár", img: "/photos/saska.jpg" },
    { name: "Artem Shtepa", role: "Frontend vývojár", img: "/photos/artem.jpg" },
    { name: "Marek Hužvár", role: "Robotik / Integrátor NAO robota (nohy)", img: "/photos/marek.jpg" },
    { name: "Maksym Liutyi", role: "Backend & Orchestration vývojár", img: "/photos/liutyi.jpg" },
    { name: "Maksym Bobukh", role: "Frontend vývojár", img: "/photos/bobukh.jpg" },
];

const WINTER_EPICS = [
    "Robot Pose & Behavior Control",
    "Backend & Frontend System",
    "Deployment & Project Presentation",
];

// ─── Helpers ─────────────────────────────────────────────────────────────────

function jump(id: string) {
    return (e: MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        const scroller = document.getElementById("left-pane");
        const target = document.getElementById(id);
        if (!scroller || !target) return;
        const top =
            target.getBoundingClientRect().top -
            scroller.getBoundingClientRect().top +
            scroller.scrollTop;
        scroller.scrollTo({ top: top - 24, behavior: "smooth" });
        history.replaceState(null, "", `#${id}`);
    };
}

// ─── UI primitives ────────────────────────────────────────────────────────────

function Divider() {
    return (
        <div className="h-px w-full my-14 bg-gradient-to-r from-transparent via-[#7c3aed]/20 to-transparent" />
    );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
    return (
        <div className="mb-8">
            <h2 className="text-3xl font-bold tracking-tight text-[#0f0e1a]">{children}</h2>
            <div className="mt-2.5 h-0.5 w-12 rounded-full bg-gradient-to-r from-[#7c3aed] to-[#4f46e5]" />
        </div>
    );
}

function DocIcon() {
    return (
        <svg className="h-4 w-4 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
    );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function Home() {
    const [activeId, setActiveId] = useState<string>("");

    useEffect(() => {
        const scroller = document.getElementById("left-pane");
        if (!scroller) return;
        const sections = Array.from(scroller.querySelectorAll("section[id]"));
        const observer = new IntersectionObserver(
            (entries) => {
                const visible = entries
                    .filter((e) => e.isIntersecting)
                    .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
                if (visible.length > 0) {
                    const id = visible[0].target.id;
                    const parentMap: Record<string, string> = {
                        minutes: "documents",
                        backlog_report: "documents",
                        sprint_retrospective: "documents",
                        methodologies: "documents",
                    };
                    setActiveId(parentMap[id] ?? id);
                }
            },
            { root: scroller, threshold: 0.9 }
        );
        sections.forEach((s) => observer.observe(s));
        return () => observer.disconnect();
    }, []);

    const navItem = (id: string, label: string, indent = false) => {
        const active = activeId === id;
        return (
            <a
                key={id}
                href={`#${id}`}
                onClick={jump(id)}
                className={[
                    "flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all duration-200",
                    indent ? "ml-3" : "",
                    active
                        ? "bg-[rgba(124,58,237,0.1)] text-[#7c3aed] font-semibold"
                        : "text-[#64748b] hover:text-[#0f0e1a] hover:bg-[#ede9fe]",
                ].join(" ")}
            >
                <span
                    className={[
                        "h-1.5 w-1.5 rounded-full flex-shrink-0 transition-all",
                        active ? "bg-[#7c3aed] scale-125" : "bg-transparent",
                    ].join(" ")}
                />
                {label}
            </a>
        );
    };

    return (
        <div className="flex grow h-screen gap-0">
            {/* ── Left pane ── */}
            <div
                id="left-pane"
                className="w-full md:w-5/7 overflow-y-auto scroll-pt-6 md:rounded-3xl md:border md:border-[#ede9fe] md:shadow-[0_0_32px_rgba(124,58,237,0.1)] md:ml-3 mt-3 mb-3 bg-white/55 backdrop-blur-sm"
            >
                <div className="px-6 md:px-14 lg:px-20 py-10 pb-40">

                    {/* ABOUT */}
                    <section id="about">
                        <SectionHeading>O projekte</SectionHeading>
                        <div className="space-y-4 leading-relaxed text-[15px]">
                            <p className="text-[#0f0e1a] font-medium text-base leading-7">
                                Projekt sa zameriava na praktický vývoj modulárneho prostredia pre simuláciu
                                a riadenie sociálnych robotov, navrhnutého na podporu interakcie človeka
                                s robotom v kontexte starostlivosti o seniorov a ich fyzickej či mentálnej aktivity.
                            </p>
                            <p className="text-[#64748b]">
                                Cieľom je rozšíriť existujúce riešenie{" "}
                                <a
                                    href="https://github.com/jperdek/socialRobotEnv"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-[#7c3aed] underline underline-offset-2 hover:no-underline"
                                >
                                    socialRobotEnv
                                </a>{" "}
                                o interaktívne a adaptívne funkcionality využiteľné v reálnych scenároch –
                                napríklad pri vedení cvičení, tréningových aktivitách, zlepšovaní pozornosti
                                alebo zábavných interakciách počas terapie so seniormi.
                            </p>
                            <p className="text-[#64748b]">
                                Riešenie je založené na architektúre samostatne nasaditeľných mikroslužieb,
                                ktoré komunikujú prostredníctvom API a sú kontajnerizované pomocou Dockeru.
                                Tento prístup zaručuje jednoduchú rozšíriteľnosť, škálovateľnosť
                                a opakovateľnosť výskumu, ako aj možnosť prispôsobenia pre rôzne robotické
                                platformy. Súčasťou projektu je aj využitie metód umelej inteligencie
                                a veľkých jazykových modelov (LLM) na podporu prirodzenej komunikácie
                                človeka s robotom.
                            </p>
                            <p className="text-[#64748b]">
                                Dlhodobým cieľom projektu je vyhodnotiť použiteľnosť takto orchestrácie
                                mikroslužieb v simulovanom aj reálnom prostredí, najmä pri interakcii
                                robota (napr. NAO) s viacerými používateľmi. Výsledky budú prispievať
                                k výskumu v oblasti sociálnej robotiky a umožnia ďalšie zdieľanie
                                Dockerizovaných nástrojov pre akademické aj terapeutické účely.
                            </p>
                        </div>
                    </section>

                    <Divider />

                    {/* EPICS */}
                    <section id="sprints">
                        <SectionHeading>Epiky</SectionHeading>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Winter */}
                            <div>
                                <p className="text-xs font-bold uppercase tracking-widest text-[#7c3aed] mb-4">
                                    Zimné epiky
                                </p>
                                <div className="space-y-3">
                                    {WINTER_EPICS.map((item, i) => (
                                        <div
                                            key={i}
                                            className="flex items-start gap-4 p-4 rounded-xl bg-white border border-[#ede9fe] shadow-sm hover:shadow-md hover:border-[rgba(124,58,237,0.3)] hover:-translate-y-px transition-all duration-200"
                                        >
                                            <span className="flex-shrink-0 h-7 w-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4f46e5] text-white text-xs font-bold flex items-center justify-center shadow-md shadow-[rgba(124,58,237,0.3)]">
                                                {i + 1}
                                            </span>
                                            <span className="pt-0.5 text-sm font-medium text-[#0f0e1a]">{item}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Summer */}
                            <div>
                                <p className="text-xs font-bold uppercase tracking-widest text-[#64748b] mb-4">
                                    Letné epiky
                                </p>
                                <div className="space-y-3">
                                    {[0, 1, 2].map((i) => (
                                        <div
                                            key={i}
                                            className="flex items-start gap-4 p-4 rounded-xl bg-white/50 border border-[#ede9fe] border-dashed"
                                        >
                                            <span className="flex-shrink-0 h-7 w-7 rounded-full bg-[#ede9fe] text-[#a78bfa] text-xs font-bold flex items-center justify-center">
                                                {i + 1}
                                            </span>
                                            <span className="pt-0.5 text-sm text-[#a78bfa] italic">Čoskoro...</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </section>

                    <Divider />

                    {/* TEAM */}
                    <section id="team">
                        <SectionHeading>Náš tím</SectionHeading>
                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 md:gap-5">
                            {TEAM.map((p) => (
                                <article
                                    key={p.name}
                                    className="group relative rounded-2xl overflow-hidden shadow-md hover:shadow-xl hover:shadow-[rgba(124,58,237,0.18)] transition-all duration-300 hover:-translate-y-1.5 cursor-default"
                                >
                                    <div className="relative aspect-[3/4] w-full">
                                        <Image
                                            src={p.img}
                                            alt={p.name}
                                            fill
                                            className="object-cover object-top transition-transform duration-500 group-hover:scale-105"
                                            priority={false}
                                            sizes="(min-width:1280px) 18vw, (min-width:768px) 26vw, 45vw"
                                        />
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/15 to-transparent" />
                                        <div className="absolute bottom-0 left-0 right-0 p-4">
                                            <h3 className="text-[13px] font-bold text-white leading-tight">{p.name}</h3>
                                            <p className="mt-1 text-[11px] text-white/65 leading-snug">{p.role}</p>
                                        </div>
                                    </div>
                                </article>
                            ))}
                        </div>
                    </section>

                    <Divider />

                    <Documents />

                    <Divider />

                    {/* CONTACTS */}
                    <section id="contacts">
                        <SectionHeading>Kontakty</SectionHeading>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="rounded-2xl overflow-hidden border border-[#ede9fe] bg-white shadow-sm hover:shadow-md transition-shadow">
                                <div className="aspect-video">
                                    <iframe
                                        title="FIIT STU – mapa"
                                        src="https://www.google.com/maps?q=FIIT%20STU%20Bratislava&output=embed"
                                        className="h-full w-full border-0"
                                        loading="lazy"
                                        referrerPolicy="no-referrer-when-downgrade"
                                    />
                                </div>
                                <div className="px-4 py-3">
                                    <p className="font-semibold text-[#0f0e1a]">FIIT STU</p>
                                    <a
                                        href="https://maps.app.goo.gl/PtXAVrcJWmcB2iYz8"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-sm text-[#7c3aed] underline underline-offset-2 hover:no-underline"
                                    >
                                        Otvoriť v Mapách
                                    </a>
                                </div>
                            </div>

                            <div className="rounded-2xl border border-[#ede9fe] bg-white shadow-sm p-6">
                                <h3 className="text-lg font-semibold mb-5 text-[#0f0e1a]">Kontakt na tím</h3>
                                <div className="flex items-center gap-4">
                                    <div className="h-10 w-10 rounded-xl bg-[rgba(124,58,237,0.1)] flex items-center justify-center flex-shrink-0">
                                        <svg className="h-5 w-5 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                        </svg>
                                    </div>
                                    <div>
                                        <p className="text-xs font-semibold uppercase tracking-widest text-[#64748b] mb-0.5">E-mail</p>
                                        <a
                                            href="mailto:tim19fiitstu@gmail.com"
                                            className="text-sm text-[#7c3aed] underline underline-offset-2 hover:no-underline"
                                        >
                                            tim19fiitstu@gmail.com
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                </div>
            </div>

            {/* ── Right nav ── */}
            <div className="w-2/7 px-3 py-3 hidden md:block">
                <div className="h-full rounded-3xl bg-white/55 backdrop-blur-sm border border-[#ede9fe] shadow-sm px-6 py-8">
                    <p className="text-xs font-bold uppercase tracking-widest text-[#7c3aed] mb-4 px-3">
                        Na tejto stránke
                    </p>
                    <nav className="flex flex-col gap-0.5">
                        {navItem("about", "O projekte")}
                        {navItem("sprints", "Epiky")}
                        {navItem("team", "Náš tím")}
                        {navItem("documents", "Dokumenty")}
                        {navItem("minutes", "Zápisnice", true)}
                        {navItem("backlog_report", "Backlog report", true)}
                        {navItem("sprint_retrospective", "Retrospektíva", true)}
                        {navItem("methodologies", "Metodiky", true)}
                        {navItem("contacts", "Kontakty")}
                    </nav>
                </div>
            </div>
        </div>
    );
}

// ─── Documents ────────────────────────────────────────────────────────────────

function DocList({ items }: { items: { label: string; href: string }[] }) {
    return (
        <ul className="mt-3 space-y-2">
            {items.map((d) => (
                <li key={d.href}>
                    <a
                        href={d.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group flex items-center gap-3 rounded-xl border border-[#ede9fe] bg-white px-4 py-3 hover:border-[rgba(124,58,237,0.3)] hover:shadow-md hover:shadow-[rgba(124,58,237,0.08)] hover:-translate-y-px transition-all duration-200"
                    >
                        <div className="flex-shrink-0 h-9 w-9 rounded-lg bg-[rgba(124,58,237,0.08)] flex items-center justify-center">
                            <DocIcon />
                        </div>
                        <span className="flex-1 text-sm font-medium text-[#0f0e1a]">{d.label}</span>
                        <span className="text-xs font-semibold text-[#7c3aed] opacity-0 group-hover:opacity-100 transition-opacity">
                            PDF →
                        </span>
                    </a>
                </li>
            ))}
        </ul>
    );
}

function SemesterLabel({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex items-center gap-3 mb-6">
            <span className="h-px flex-1 bg-[#ede9fe]" />
            <span className="text-xs font-bold uppercase tracking-widest text-[#64748b] whitespace-nowrap">
                {children}
            </span>
            <span className="h-px flex-1 bg-[#ede9fe]" />
        </div>
    );
}

function DocSubSection({ label, children }: { label: string; children: React.ReactNode }) {
    return (
        <div>
            <p className="text-xs font-bold uppercase tracking-widest text-[#7c3aed] mb-2">{label}</p>
            {children}
        </div>
    );
}

function EmptyDocList() {
    return (
        <p className="mt-3 text-sm text-[#a78bfa] italic px-1">Čoskoro...</p>
    );
}

function Documents() {
    return (
        <section id="documents">
            <SectionHeading>Dokumenty</SectionHeading>

            {/* ZIMNÝ SEMESTER */}
            <div className="rounded-2xl border border-[#ede9fe] bg-white/60 p-6">
                <SemesterLabel>Zimný semester</SemesterLabel>

                <section id="minutes">
                    <DocSubSection label="Zápisnice">
                        <DocList items={DOCS.minutes} />
                    </DocSubSection>
                </section>

                <section id="backlog_report" className="mt-7">
                    <DocSubSection label="Backlog report">
                        <DocList items={DOCS.backlog} />
                    </DocSubSection>
                </section>

                <section id="sprint_retrospective" className="mt-7">
                    <DocSubSection label="Retrospektíva šprintov">
                        <DocList items={DOCS.retrospective} />
                    </DocSubSection>
                </section>
            </div>

            {/* LETNÝ SEMESTER */}
            <div className="mt-5 rounded-2xl border border-[#ede9fe] bg-white/60 p-6">
                <SemesterLabel>Letný semester</SemesterLabel>

                <section id="minutes_summer">
                    <DocSubSection label="Zápisnice">
                        {DOCS.minutes_summer.length > 0
                            ? <DocList items={DOCS.minutes_summer} />
                            : <EmptyDocList />}
                    </DocSubSection>
                </section>

                <section id="backlog_report_summer" className="mt-7">
                    <DocSubSection label="Backlog report">
                        {DOCS.backlog_summer.length > 0
                            ? <DocList items={DOCS.backlog_summer} />
                            : <EmptyDocList />}
                    </DocSubSection>
                </section>

                <section id="sprint_retrospective_summer" className="mt-7">
                    <DocSubSection label="Retrospektíva šprintov">
                        {DOCS.retrospective_summer.length > 0
                            ? <DocList items={DOCS.retrospective_summer} />
                            : <EmptyDocList />}
                    </DocSubSection>
                </section>
            </div>

            {/* METODIKY — bez semestra */}
            <section id="methodologies" className="mt-10">
                <p className="text-xs font-bold uppercase tracking-widest text-[#7c3aed] mb-2">Metodiky</p>
                <DocList items={DOCS.methodologies} />
            </section>
        </section>
    );
}
