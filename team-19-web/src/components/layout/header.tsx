import Image from "next/image";

type HeaderProps = {
    img_src: string;
    project_name: string;
    team_number: number;
};

export default function Header({ img_src, project_name, team_number }: HeaderProps) {
    return (
        <header
            className="
        flex items-center justify-between
        border-[var(--lines)]/20 border-b-[0.5px] border-r-[0.5px]
        shadow-[0_0_10px_var(--container)]
        rounded-b-3xl
        px-4 sm:px-8 md:px-12 lg:px-20
        py-3 md:py-4
        mx-0 md:mx-4
        flex-wrap gap-3 sm:gap-4
      "
        >

            <div className="flex items-center gap-3 sm:gap-4 min-w-0">
                <Image
                    src={img_src}
                    alt="neo robot head"
                    width={48}
                    height={48}
                    className="flex-shrink-0"
                />
                <h1
                    className="
            text-lg sm:text-xl font-semibold truncate
            max-w-[200px] sm:max-w-[400px] md:max-w-[500px] lg:max-w-[900px]
          "
                    title={project_name}
                >
                    {project_name}
                </h1>
            </div>

            <h1 className="text-base sm:text-lg md:text-xl font-semibold whitespace-nowrap">
                Tím {team_number}
            </h1>
        </header>
    );
}
