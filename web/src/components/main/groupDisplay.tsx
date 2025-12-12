import { Card, CardPerson} from "@/components/ui/card";
import { User} from "lucide-react";

interface Person {
  id: number;
  name: string;
  statistics: string;
  attendance: string;
}

interface PersonDisplayProps {
  people: Person[];
}

export function GroupDisplay({ people }: PersonDisplayProps) {
  return (
    <Card className="shadow-lg w-full">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {people.map((person) => (
          <Card key={person.id} className=" shadow w-full">
            <CardPerson className=" text-center">
              <div className="w-full flex items-center">
                <User className="mr-1" />
                <h3 className="font-bold text-lg">{person.name}</h3>
              </div>

              {person.statistics && (
                <p className="text-sm mt-2">{person.statistics}</p>
              )}
              {person.attendance && (
                <p className="text-sm mt-2">{person.attendance}</p>
              )}
            </CardPerson>
          </Card>
        ))}
      </div>
    </Card>
  );
}
