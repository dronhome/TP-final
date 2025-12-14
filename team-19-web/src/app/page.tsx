"use client";

import Image from "next/image";

import { useEffect, useState, MouseEvent } from "react";

const DOCS = {
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
    methodologies: [
        { label: "Metodika komunikácie", href: "/docs/methodologies/Metodika-komunikácie.pdf " },
        { label: "Metodika revízie kódu", href: "/docs/methodologies/Metodika-revízieKódu.pdf" },
        { label: "Metodika spravovania backlogu", href: "/docs/methodologies/Metodika-spravovaniaBacklogu.pdf" },
        { label: "Metodika práce s robotom", href: "/docs/methodologies/Metodika-prácesRobotom.pdf" },
        { label: "Metodika spracovania videí", href: "/docs/methodologies/Metodika-spracovaniaVideí.pdf" },


    ],
};


function jump(id: string) {
    return (e: MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        const scroller = document.getElementById("left-pane");
        const target = document.getElementById(id);
        if (!scroller || !target) return;

        const topWithinScroller =
            target.getBoundingClientRect().top -
            scroller.getBoundingClientRect().top +
            scroller.scrollTop;

        const HEADER_H = 20;

        scroller.scrollTo({
            top: topWithinScroller - HEADER_H,
            behavior: "smooth",
        });

        history.replaceState(null, "", `#${id}`);
    };
}

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

    const linkClasses = (id: string) =>
        `transition-colors ${
            activeId === id ? "text-[var(--container)] font-semibold" : "text-[var(--foreground)]"
        } hover:text-[var(--container)]`;

    return (
        <div className="flex grow h-screen">
            <div
                id="left-pane"
                className="w-full md:w-5/7 overflow-y-auto scroll-pt-[72px] md:rounded-3xl md:shadow-[0_0_10px_var(--container)] md:border-[var(--lines)]/20 md:border-t-[0.5px] md:border-r-[0.5px] p-5 md:ml-5 mt-5"
            >
                <div className="px-5 md:px-20 p-5 pb-20  md:pb-60">
                    <section id="about" className="mb-10 leading-relaxed ">
                        <h2 className="info-section">O projekte</h2>
                        <p>
                            Projekt sa zameriava na praktický vývoj modulárneho prostredia pre simuláciu a riadenie
                            sociálnych robotov, navrhnutého na podporu interakcie človeka s robotom v kontexte
                            starostlivosti o seniorov a ich fyzickej či mentálnej aktivity. Cieľom je rozšíriť
                            existujúce riešenie{" "}
                            <a
                                href="https://github.com/jperdek/socialRobotEnv"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[var(--container)] underline hover:no-underline"
                            >
                                socialRobotEnv
                            </a>{" "}
                            o interaktívne a adaptívne funkcionality využiteľné v reálnych scenároch – napríklad
                            pri vedení cvičení, tréningových aktivitách, zlepšovaní pozornosti alebo zábavných
                            interakciách počas terapie so seniormi.
                        </p>

                        <p className="mt-4">
                            Riešenie je založené na architektúre samostatne nasaditeľných mikroslužieb, ktoré
                            komunikujú prostredníctvom API a sú kontajnerizované pomocou Dockeru. Tento prístup
                            zaručuje jednoduchú rozšíriteľnosť, škálovateľnosť a opakovateľnosť výskumu, ako aj
                            možnosť prispôsobenia pre rôzne robotické platformy. Súčasťou projektu je aj využitie
                            metód umelej inteligencie a veľkých jazykových modelov (LLM) na podporu prirodzenej
                            komunikácie človeka s robotom.
                        </p>

                        <p className="mt-4">
                            Dlhodobým cieľom projektu je vyhodnotiť použiteľnosť takto orchestrácie mikroslužieb
                            v simulovanom aj reálnom prostredí, najmä pri interakcii robota (napr. NAO) s viacerými
                            používateľmi. Výsledky budú prispievať k výskumu v oblasti sociálnej robotiky a umožnia
                            ďalšie zdieľanie Dockerizovaných nástrojov pre akademické aj terapeutické účely.
                        </p>
                    </section>

                    <div className="h-[1px] w-full bg-[var(--container)] mb-10 mt-2 mb-12"></div>


                    <section id="sprints" className="mb-10">
                        <h2 className="info-section ">Epiky</h2>

                        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-12">

                            <div>
                                <p className="sub-info-section mb-4 font-semibold text-center">Zimné epiky</p>

                                <div className="relative pl-8">
                                    <div className="absolute left-3 top-0 bottom-0 w-[3px] bg-[var(--container)]/40 -z-10"></div>

                                    {[
                                        "Robot Pose & Behavior Control",
                                        "Backend & Frontend System",
                                        "Deployment & Project Presentation",
                                    ].map((item, i) => (
                                        <div key={i} className="relative mb-6 last:mb-0">

                                            <div className="absolute left-[-3px] top-1/2 -translate-y-1/2 h-3 w-3 rounded-full bg-[var(--container)] shadow-[0_0_6px_var(--container)]"></div>


                                            <div className="ml-6 rounded-xl border border-[var(--lines)] bg-[var(--background)] px-6 py-3 shadow-[0_0_8px_var(--container)]">
                                                {item}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <p className="sub-info-section mb-4 font-semibold text-center">Letné epiky</p>

                                <div className="relative pl-8">
                                    <div className="absolute left-3 top-0 bottom-0 w-[3px] bg-[var(--container)]/40 -z-10"></div>

                                    {[
                                        "",
                                        "",
                                        "",
                                    ].map((item, i) => (
                                        <div key={i} className="relative mb-6 last:mb-0">
                                            <div className="absolute left-[-3px] top-1/2 -translate-y-1/2 h-3 w-3 rounded-full bg-[var(--container)] shadow-[0_0_6px_var(--container)]"></div>

                                            <div className="ml-6 rounded-xl border border-[var(--lines)] bg-[var(--background)] px-6 py-3 shadow-[0_0_8px_var(--container)]">
                                                {item}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </section>




                    <div className="h-[1px] w-full bg-[var(--container)] mb-10"></div>




                    <section id="team" className="mb-10">
                        <h2 className="info-section">Náš tím</h2>

                        <div className="mt-6 grid grid-cols-[repeat(auto-fit,minmax(220px,1fr))] gap-6">
                            {[
                                { name: "Andrii Kostiushko", role: "Projektový manažér, Robotik / Integrátor NAO robota (ruky)", img: "/photos/andrii_k.jpg" },
                                { name: "Oleksandra Pozdniakova", role: "Frontend vývojár", img: "/team/x.jpg" },
                                { name: "Artem Shtepa", role: "Frontend vývojár", img: "/team/x.jpg" },
                                { name: "Marek Hužvár", role: "Robotik / Integrátor NAO robota (nohy)", img: "/team/x.jpg" },
                                { name: "Maksym Liutyi", role: "Backend & Orchestration vývojár", img: "/team/x.jpg" },
                                { name: "Maksym Bobukh", role: "Frontend vývojár", img: "/team/x.jpg" },
                            ].map((p) => (
                                <article
                                    key={p.name}
                                    className="rounded-2xl border border-[var(--lines)] bg-[var(--background)] shadow-[0_0_10px_var(--container)]/40 overflow-hidden"
                                >

                                    <div className="relative aspect-square w-full">
                                        <Image
                                            src={p.img}
                                            alt={p.name}
                                            fill
                                            className="object-cover"
                                            priority={false}
                                            sizes="(min-width:1280px) 25vw, (min-width:1024px) 33vw, (min-width:640px) 50vw, 100vw"

                                        />
                                    </div>

                                    <div className="p-4">
                                        <h3 className="text-lg font-semibold line-clamp-1">{p.name}</h3>
                                        <p className="mt-1 text-sm text-[var(--foreground)] line-clamp-2">
                                            {p.role}
                                        </p>
                                    </div>
                                </article>
                            ))}
                        </div>
                    </section>


                    <div className="h-[1px] w-full bg-[var(--container)] mb-10"></div>

                    <Documents/>

                    <div className="h-[1px] w-full bg-[var(--container)] mb-10"></div>


                    <section id="contacts" className="mb-10">
                        <h2 className="info-section">Kontakty</h2>

                        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-8">

                            <div className="rounded-2xl border border-[var(--lines)]/40 shadow-[0_0_10px_var(--container)] overflow-hidden">
                                <div className="aspect-video">

                                    <iframe
                                        title="FIIT STU – mapa"
                                        src="https://www.google.com/maps?q=FIIT%20STU%20Bratislava&output=embed"
                                        className="h-full w-full border-0"
                                        loading="lazy"
                                        referrerPolicy="no-referrer-when-downgrade"
                                    />
                                </div>

                                <div className="flex items-center justify-between px-4 py-3">
                                    <div>
                                        <p className="font-semibold">FIIT STU</p>

                                        <a
                                            href="https://maps.app.goo.gl/PtXAVrcJWmcB2iYz8"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-sm text-[var(--container)] underline hover:no-underline"
                                        >
                                            Otvoriť v Mapách
                                        </a>
                                    </div>
                                </div>
                            </div>

                            <div className="rounded-2xl border border-[var(--lines)]/40 shadow-[0_0_10px_var(--container)] p-6">
                                <h3 className="text-xl font-semibold mb-3">Kontakt na tím</h3>

                                <div className="space-y-3">
                                    <div className="flex items-center gap-3">
                                        <span className="h-2.5 w-2.5 rounded-full bg-[var(--container)] shadow-[0_0_6px_var(--container)]" />
                                        <span>E-mail:</span>
                                        <a
                                            href="mailto:tim19fiitstu@gmail.com"
                                            className="text-[var(--container)] underline hover:no-underline"
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

            {/* RIGHT NAVIGATION */}
            <div className="w-2/7 pl-5 pr-5 pt-5 pb-5 hidden md:block">
                <div className="h-[100%] rounded-3xl shadow-[0_0_10px_var(--container)] border-[var(--lines)]/20 border-b-[0.5px] border-l-[0.5px] border-t-[0.5px] p-10">
                    <h1 className="text-heading">Na tejto stránke:</h1>

                    <nav className="flex flex-col gap-2 py-3">
                        <a href="#about" onClick={jump("about")} className={linkClasses("about")}>
                            O projekte
                        </a>
                        <a href="#epics" onClick={jump("epics")} className={linkClasses("epics")}>
                            Epiky
                        </a>
                        <a href="#team" onClick={jump("team")} className={linkClasses("team")}>
                            Náš tím
                        </a>
                        <a href="#documents" onClick={jump("documents")} className={linkClasses("documents")}>
                            Dokumenty
                        </a>

                        <div className="ml-3 flex flex-col gap-2">
                            <a href="#minutes" onClick={jump("minutes")} className={linkClasses("minutes")}>
                                Zápisnice
                            </a>
                            <a href="#backlog_report" onClick={jump("backlog_report")} className={linkClasses("backlog_report")}>
                                Backlog report
                            </a>
                            <a href="#sprint_retrospective" onClick={jump("sprint_retrospective")} className={linkClasses("sprint_retrospective")}>
                                Retrospektíva šprintov
                            </a>
                            <a href="#methodologies" onClick={jump("methodologies")} className={linkClasses("methodologies")}>
                                Metodiky
                            </a>
                        </div>



                        <a href="#contacts" onClick={jump("contacts")} className={linkClasses("contacts")}>
                            Kontakty
                        </a>
                    </nav>
                </div>
            </div>
        </div>
    );
}


function DocList({ items }: { items: { label: string; href: string }[] }) {
    return (
        <ul className="mt-4 space-y-3">
            {items.map((d) => (
                <li key={d.href}>
                    <a
                        href={d.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group flex items-center gap-3 rounded-lg border border-[var(--lines)]/40 bg-[var(--background)] px-4 py-3 hover:shadow-[0_0_10px_var(--container)] transition-shadow"
                    >
                        <span className="h-2.5 w-2.5 rounded-full bg-[var(--container)] shadow-[0_0_6px_var(--container)]" />
                        <span className="flex-1">{d.label}</span>
                        <span className="text-sm text-[var(--container)] opacity-80 group-hover:opacity-100">Otvoriť PDF</span>
                    </a>
                </li>
            ))}
        </ul>
    );
}

function Documents() {
    return (
        <section id="documents" className="mb-10">
            <h2 className="info-section">Dokumenty</h2>

            {/* ZÁPISNICE */}
            <section id="minutes" className="mt-8">
                <h3 className="sub-info-section font-semibold">Zápisnice</h3>
                <DocList items={DOCS.minutes} />
            </section>

            {/* BACKLOG REPORT */}
            <section id="backlog_report" className="mt-10">
                <h3 className="sub-info-section font-semibold">Backlog report</h3>
                <DocList items={DOCS.backlog} />
            </section>

            {/* RETROSPEKTÍVA ŠPRINTOV */}
            <section id="sprint_retrospective" className="mt-10">
                <h3 className="sub-info-section font-semibold">Retrospektíva šprintov</h3>
                <DocList items={DOCS.retrospective} />
            </section>

            {/* METODIKY */}
            <section id="methodologies" className="mt-10">
                <h3 className="sub-info-section font-semibold">Metodiky</h3>
                <DocList items={DOCS.methodologies} />
            </section>
        </section>
    );
}
