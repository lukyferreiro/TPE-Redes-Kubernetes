import React from "react";

export const Player = ({player}) => {
    return (<div className="glass p-5">
        <h1 className="text-2xl font-bold">{player.name}</h1>
        <div className="flex flex-col">
            <p><span className="font-bold">Name:</span> {player.name}</p>
            {player.full_name && <p><span className="font-bold">Full name:</span> {player.full_name}</p>}
            <p><span className="font-bold">Age:</span> {player.age}</p>
            <p><span className="font-bold">Height (cm):</span> {player.height_cm}</p>
            <p><span className="font-bold">Weight (kgs):</span> {player.weight_kgs}</p>
            {player.score && <p><span className="font-bold">Positions:</span> {player.positions}</p>}
            {player.score && <p><span className="font-bold">Nationality:</span> {player.nationality}</p>}
            {player.score && <p><span className="font-bold">Overall rating:</span> {player.overall_rating}</p>}
            {player.score && <p><span className="font-bold">Potential:</span> {player.potential}</p>}
        </div>
    </div>);
};
