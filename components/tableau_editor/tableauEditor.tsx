import { Table, useMantineTheme,ScrollArea,SimpleGrid , Box, useComputedColorScheme, Paper, Grid, Text, PinInput } from "@mantine/core"
import {useState, useRef} from "react";



export const TableauEditor = ({size}: {size : number})  => {
    
    const [isActive, setIsActive] = useState(false);
    const cellRef = useRef<HTMLElement>(null)!;
    const handleClick = () => {
        if(cellRef.current)
        {
            cellRef.current.style.backgroundColor = 'blue';
        }
    };
    console.log("rerendering")
    return (
        <>
        
            <ScrollArea w="100%" className="relative">
                <canvas id="myCanvas" className=" h-[50vw] bg-gray-500 absolute"></canvas>
                <div  style={{ minWidth: 400}} >
                    {[...Array(size+1)].map((_,index) => (
                        
                        <Box
                        name="pin"
                        length={4}
                        oneTimeCode
                        gap={0}
                        radius={0}/>
                    
                    ))}
                </div >
            </ScrollArea>


        </>
    )
}