import { DependencyContainer } from "tsyringe";

import { IPostDBLoadMod } from "@spt-aki/models/external/IPostDBLoadMod";

class Mod implements IPostDBLoadMod
{
    public postDBLoad(container: DependencyContainer): void 
    {
        console.log("hello")
    }
}

module.exports = { mod: new Mod() }