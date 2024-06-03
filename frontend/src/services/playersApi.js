import axios from "axios";

const apiAxios = axios.create();

export const playersApi = {
    getPlayers: async (version, name, signal) => {
        const response = await apiAxios.get(`http://api.players.com:5000/${version}/players`, {
            params: {
                name,
            },
            signal,
        });

        return {
            clusterData: {
                nodeName: response.headers['x-node-name'],
                nodeIp: response.headers['x-node-ip'],
                podIp: response.headers['x-pod-ip'],
                podName: response.headers['x-pod-name'],
                podNamespace: response.headers['x-pod-namespace'],
                podUid: response.headers['x-pod-uid'],
                podServiceAccount: response.headers['x-pod-service-account'],
            }, players: response.data,
        }
    },
};