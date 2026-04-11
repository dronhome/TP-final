import Image from "next/image";

type HeaderProps = {
    img_src: string;
    project_name: string;
    team_number: number;
};

export default function Header({ img_src, project_name, team_number }: HeaderProps) {
    return (
        <header className="flex items-center justify-between mx-3 mt-3 px-5 sm:px-8 py-3 rounded-2xl bg-white/70 backdrop-blur-md border border-[#ede9fe] shadow-sm">
            <div className="flex items-center gap-3 min-w-0">
                <div className="flex-shrink-0 h-10 w-10 rounded-xl bg-gradient-to-br from-[#7c3aed] to-[#4f46e5] flex items-center justify-center shadow-md shadow-[rgba(124,58,237,0.25)]">
                    <Image
                        src={img_src}
                        alt="logo"
                        width={26}
                        height={26}
                        className="brightness-0 invert"
                    />
                </div>
                <h1
                    className="text-sm sm:text-base font-semibold truncate text-[#0f0e1a] max-w-[200px] sm:max-w-[420px] md:max-w-[600px] lg:max-w-[900px]"
                    title={project_name}
                >
                    {project_name}
                </h1>
            </div>

            <span className="flex-shrink-0 text-xs font-semibold px-3 py-1.5 rounded-full bg-[rgba(124,58,237,0.1)] text-[#7c3aed] border border-[rgba(124,58,237,0.2)] whitespace-nowrap">
                Tím {team_number}
            </span>
        </header>
    );
}
