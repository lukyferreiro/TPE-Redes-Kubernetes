import React from "react";

export const ClusterData = ({clusterData}) => {
    return (<div className="glass p-5">
        <div className="flex flex-col">
            <p className="text-xl"><span className="font-bold">Node Name: </span>{clusterData.nodeName}</p>
            <p className="text-xl"><span className="font-bold">Node IP: </span>{clusterData.nodeIp}</p>
            <p className="text-xl"><span className="font-bold">Pod IP: </span>{clusterData.podIp}</p>
            <p className="text-xl"><span className="font-bold">Pod Name: </span>{clusterData.podName}</p>
            <p className="text-xl"><span className="font-bold">Pod Namespace: </span>{clusterData.podNamespace}</p>
            <p className="text-xl"><span className="font-bold">Pod UID: </span>{clusterData.podUid}</p>
            <p className="text-xl"><span className="font-bold">Pod Service Account: </span>{clusterData.podServiceAccount}</p>
        </div>
    </div>);
};
