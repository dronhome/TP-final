import { Header } from "../components/layout/header";
import { BottomNav } from "../components/layout/bottomNav";
import { GroupDisplay } from "@/components/main/groupDisplay"

export default function GroupPage() {

    const peopleList = [
    { id: 1, name: "Mike", statistics:  "Statistics: ...", attendance: "Attendance: ..." },
    { id: 2, name: "Maria", statistics:  "Statistics: ...", attendance: "Attendance: ..." },
    { id: 3, name: "Klara", statistics:  "Statistics: ...", attendance: "Attendance: ..." },
    { id: 4, name: "Ivan", statistics:  "Statistics: ...", attendance: "Attendance: ..." },
  ];
    return (
          <div className="w-full max-w-sm rounded-md ">
            <Header title="Skupina" />
            <div className="mt-4">
              <GroupDisplay people={peopleList}/>
              <BottomNav />
            </div>
          </div>
      );
    }