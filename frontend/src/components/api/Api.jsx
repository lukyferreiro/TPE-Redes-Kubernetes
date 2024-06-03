import React from "react";
import {useForm} from "react-hook-form";
import {playersApi} from "@/services/playersApi.js";
import {useQuery, useQueryClient} from "@tanstack/react-query";
import {Player} from "@components/player/Player.jsx";
import {ClusterData} from "@components/cluster-data/ClusterData.jsx";
import {HashLoader} from "react-spinners";

export const Api = ({apiVersion}) => {
    const {register, handleSubmit} = useForm();
    const playerName = React.useRef("");

    const {
        data: {players, clusterData} = {}, isFetching, isError, refetch,
    } = useQuery({
        queryKey: [`api${apiVersion}players`],
        queryFn: async ({signal}) => {
            return await playersApi.getPlayers(apiVersion, playerName.current, signal);
        },
        enabled: false,
    });

    const queryClient = useQueryClient()

    const onSubmit = (data) => {
        queryClient.cancelQueries({ queryKey: [`api${apiVersion}players`] })
        playerName.current = data.player;
        refetch();
    };

    return (
        <div className="basis-1/2 flex flex-col gap-5 p-10">
            <div className="flex flex-col justify-start items-stretch gap-3">
                <h1 className="text-5xl font-semibold text-center">
                    API {apiVersion.toUpperCase()}
                </h1>
                <form onSubmit={handleSubmit(onSubmit)}
                      className="flex flex-col align-stretch justify-center gap-5">
                    <input {...register("player")}
                        className="flex-1 p-5 rounded border-2 border-gray-400/50 bg-transparent"
                        placeholder={`Search a player in API ${apiVersion.toUpperCase()}`}
                    />
                </form>
            </div>

            {!!players && !isFetching &&
                <>
                    <h1 className="text-3xl font-bold">Node and POD Information</h1>
                    <ClusterData clusterData={clusterData}/>
                    <h1 className="text-3xl text-center font-bold">Players</h1>
                    <div className="grid grid-cols-2 gap-4">
                        {players.map((player) =>
                            <Player key={player.id} player={player}/>
                        )}
                    </div>
                </>
            }

            {isFetching &&
                <div className="flex flex-row justify-center items-center h-48">
                    <HashLoader color="#36d7b7"/>
                </div>
            }
        </div>
    )
};
